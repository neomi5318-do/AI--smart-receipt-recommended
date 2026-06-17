from fastapi import APIRouter, File, UploadFile
# ייבוא של הלוגיקה מהקונטרולר שלנו
from app.controllers.detection_controller import process_image_for_ingredients

# במקום app = FastAPI(), פה אנחנו משתמשים ב-Router
router = APIRouter()

@router.post("/detect")
async def detect_ingredients(file: UploadFile = File(...)):
    # 1. קוראים את הקובץ שהמשתמש העלה
    contents = await file.read()
    
    # 2. מעבירים לקונטרולר שיפעיל את ה-AI
    detected_items = process_image_for_ingredients(contents)
    
    # 3. מחזירים תשובה מסודרת חזרה למשתמש
    return {
        "status": "success",
        "detected_ingredients": detected_items
    }