# app/routes/recipes_route.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.controllers.recipes_controller import get_recommended_recipes

router = APIRouter()

# מבנה הבקשה שהריאקט ישלח אלינו
class IngredientsRequest(BaseModel):
    detected_ingredients: list[str]

@router.post("/recommend")
def recommend_recipes(request: IngredientsRequest, db: Session = Depends(get_db)):
    # מעבירים לקונטרולר את החיבור לדאטהבייס ואת רשימת המצרכים מהבקשה
    recipes = get_recommended_recipes(db, request.detected_ingredients)
    
    return {
        "status": "success",
        "recipes": recipes
    }