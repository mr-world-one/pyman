from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
import os
import requests
from datetime import datetime
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.model import User

router = APIRouter(prefix="/assistant", tags=["Assistant"])

# Hugging Face API ключ
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_MODEL_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

class AssistantRequest(BaseModel):
    task: str
    message: Optional[str] = None

class AssistantResponse(BaseModel):
    status: str
    response: Optional[str] = None
    timestamp: str

def query_huggingface_api(message: str) -> str:
    """
    Використовує API Hugging Face для генерації відповіді.
    """
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    prompt = f"""<|system|>You are an assistant for the CheckIT project, a platform designed to analyze and compare tender proposals, both public and private. Your role is to provide accurate and detailed answers about the project's functionality, features, and technical aspects. The platform includes features like user registration, CRUD operations, XPath analysis for web scraping, AI-powered assistance, and integration with Prozorro for tender analysis. If the user's question is unrelated to the project, politely inform them that you can only assist with questions about CheckIT. Use Ukrainian to answer(Not Russian)<|endoftext|><|user|>{message}<|endoftext|><|assistant|>"""
    try:
        response = requests.post(
            HUGGINGFACE_MODEL_URL,
            headers=headers,
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 100,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            },
            timeout=10
        )

        if response.status_code != 200:
            raise Exception(f"Помилка API Hugging Face: {response.status_code}, {response.text}")

        result = response.json()

        # Перевіряємо, чи результат є списком
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "Не вдалося згенерувати відповідь.")
        else:
            raise Exception("Неправильний формат відповіді від Hugging Face API.")

    except requests.exceptions.Timeout:
        raise Exception("Запит до Hugging Face API перевищив час очікування.")
    except Exception as e:
        raise Exception(f"Помилка при використанні Hugging Face API: {str(e)}")

@router.post("/perform-task", response_model=AssistantResponse)
async def perform_task(request: AssistantRequest, db: AsyncSession = Depends(get_db)):
    """
    Багатофункціональний помічник для виконання завдань.
    """
    try:
        task = request.task.lower()
        message = request.message

        if task == "time":
            # Повертає поточний час
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return AssistantResponse(
                status="success",
                response=f"Поточний час: {current_time}",
                timestamp=current_time
            )

        elif task == "chat":
            # Використовує Hugging Face API для відповіді на запит
            if not message:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Для завдання 'chat' необхідно надати повідомлення."
                )

            try:
                response_text = query_huggingface_api(message)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Помилка при використанні Hugging Face API: {str(e)}"
                )

            return AssistantResponse(
                status="success",
                response=response_text,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

        elif task == "help":
            # Повертає список доступних завдань
            return AssistantResponse(
                status="success",
                response=(
                    "Доступні завдання:\n"
                    "- `time`: Повертає поточний час.\n"
                    "- `chat`: Відповідає на ваші запити за допомогою AI.\n"
                    "- `user_count`: Повертає кількість зареєстрованих користувачів.\n"
                    "- `help`: Показує список доступних завдань."
                ),
                timestamp=datetime.now().strftime("%Y-%м-%d %H:%М:%S")
            )

        elif task == "user_count":
            # Повертає кількість зареєстрованих користувачів
            result = await db.execute(select(User))
            users = result.scalars().all()
            user_count = len(users)
            return AssistantResponse(
                status="success",
                response=f"Кількість зареєстрованих користувачів на нашому сервісі: {user_count}",
                timestamp=datetime.now().strftime("%Y-%м-%d %H:%М:%S")
            )

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Невідоме завдання: {task}. Використовуйте 'help' для списку доступних завдань."
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Помилка сервера: {str(e)}"
        )