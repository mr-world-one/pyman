#third-party imports
from fastapi import APIRouter, HTTPException

#local imports
from app.prozorro_functionality.prozorro import get_contract_info

prozorro_router = APIRouter()

@prozorro_router.get("/contract_info/{contract_id}")
def tender_items(contract_id: str):
    return get_contract_info(contract_id)


