#third-party imports
from fastapi import APIRouter, HTTPException

#local imports
from app.prozorro_functionality.prozorro import get_contract_info

import sys
sys.path.append("C:\\Users\\it-support\\pyman")  
from fastapi import FastAPI, HTTPException, Depends
import asyncpg
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
import logging
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from scraper.parsers.rozetka_parser import RozetkaParser
from fastapi import FastAPI, File, UploadFile
from statistics import mean
import logging
from io import BytesIO
from openpyxl import load_workbook
from pydantic import BaseModel
from typing import List, Optional
from app.prozorro_functionality.prozorro import get_contract_info
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
import time
import re

prozorro_router = APIRouter()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# @prozorro_router.get("/contract_info/{contract_id}")
# def tender_items(contract_id: str):
#     return get_contract_info(contract_id)

@prozorro_router.get("/search-tender/{contract_id}")
def prozorro_data(contract_id : str):
    rozetka = RozetkaParser()
    try:
        pr_data = get_contract_info(contract_id)
        d = [] 
        
        for row in pr_data:
            product_name = row['name']
            logger.info(f"Searching for: '{product_name}'")
            try:
                rozetka_data = rozetka.find_n_products(
                    product=product_name,
                    n=1,
                    fast_parse=False,
                    ignore_price_format=True,
                    raise_exception=False
                )
                d.extend(rozetka_data)
                logger.info(f"Success: Found {len(rozetka_data)} products for '{product_name}'")
            except Exception as e:
                logger.warning(f"No result for '{product_name}': {str(e)}")
                continue
        
        # Повертаємо обидва набори даних
        return {
            "status": "success",
            "message": "Products found",
            "prozorro_data": pr_data,  # Дані з Excel
            "rozetka_data": d          # Дані з Rozetka
        }
    except Exception as e:
        logger.error(f"Error in upload_excel: {str(e)}")
        return str(e)


