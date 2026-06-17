# app/main.py

from fastapi import FastAPI
# ייבוא הראוטרים שלנו
from app.routes import detection_route
from app.routes import recipes_route

app = FastAPI()

# מחברים את הראוטרים תחת הקידומת /api
app.include_router(detection_route.router, prefix="/api/detection", tags=["Detection"])
app.include_router(recipes_route.router, prefix="/api/recipes", tags=["Recipes"])

@app.get("/")
def read_root():
    return {"status": "השרת פועל בהצלחה!", "project": "Smart Recipe Recommender"}