import cv2
import numpy as np
from ultralytics import YOLO

# טעינת המודל - אנחנו עושים את זה מחוץ לפונקציה כדי שייטען פעם אחת כשהשרת עולה
# ולא בכל פעם שמשתמש שולח תמונה (זה יחסוך המון זמן!)
model = YOLO("yolov8s-world.pt")

model.set_classes([
    "milk", "egg", "cheese", "butter", 
    "tomato", "cucumber", "chicken", 
    "ketchup", "onion", "garlic", "yogurt"
])

def process_image_for_ingredients(image_bytes: bytes) -> list:
    """
    פונקציה זו מקבלת תמונה כבייטים, מעבירה אותה דרך מודל ה-YOLO
    ומחזירה רשימה של מצרכים שזוהו.
    """
    # המרה לפורמט ש-OpenCV מבין
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # הרצת המודל על התמונה
    results = model(image)
    
    detected_items = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            label = model.names[class_id] 
            
            if label not in detected_items:
                detected_items.append(label)
                
    return detected_items