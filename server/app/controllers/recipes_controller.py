# app/controllers/recipes_controller.py

from sqlalchemy.orm import Session
from app.models.recipe import Recipe

def get_recommended_recipes(db: Session, detected_ingredients: list[str]):
    # 1. שליפת כל המתכונים מהטבלה באמצעות ה-ORM
    all_recipes = db.query(Recipe).all()
    
    recommended = []
    
    # הופכים את המצרכים שזוהו לאותיות קטנות כדי למנוע בעיות של רגישות לאותיות גדולות/קטנות
    detected_set = set(item.lower() for item in detected_ingredients)
    
    for recipe in all_recipes:
        # בגלל שהגדרתן JSON, פייתון כבר מתייחס לזה כאל רשימה
        recipe_ingredients = [item.lower() for item in recipe.ingredients]
        
        # חיתוך (Intersection) - בודק אילו מצרכים מהתמונה קיימים במתכון
        matches = detected_set.intersection(set(recipe_ingredients))
        
        if matches:  # אם יש לפחות מצרך אחד שמתאים
            recommended.append({
                "id": recipe.id,
                "name": recipe.name,
                "instructions": recipe.instructions,
                "prep_time": recipe.prep_time,
                "match_count": len(matches),      # כמות המצרכים שהתאימו
                "matched_items": list(matches)    # אילו מצרכים בדיוק התאימו
            })
            
    # מיון מההתאמה הגבוהה ביותר (הכי הרבה מצרכים תואמים) לנמוכה ביותר
    recommended.sort(key=lambda x: x["match_count"], reverse=True)
    
    return recommended