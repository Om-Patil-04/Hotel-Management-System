import joblib
import numpy as np
from typing import Dict
from config.paths_config import MODEL_OUTPUT_PATH


class PredictPipeline:
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not PredictPipeline._initialized:
            artifact = joblib.load(MODEL_OUTPUT_PATH)
            
            self.model = artifact["model"]
            self.threshold = artifact["threshold"]
            self.features = artifact["features"]
            self.model_name = artifact["model_name"]
            self.encoders = artifact.get("encoders", None)
            self.scaler = artifact.get("scaler", None)
            
            print(f"Loaded model: {self.model_name}")
            print(f"Threshold  : {self.threshold}")
            
            PredictPipeline._initialized = True
    
    def predict(self, input_data: Dict[str, float]) -> Dict:
        X = np.array([input_data[col] for col in self.features]).reshape(1, -1)
        
        if self.scaler:
            X = self.scaler.transform(X)
        
        proba_not_canceled = self.model.predict_proba(X)[0, 1]
        prediction = int(proba_not_canceled >= self.threshold)
        
        result = {
            "model_name": self.model_name,
            "prediction": "Not Canceled" if prediction else "Canceled",
            "prediction_label": prediction,
            "probability": float(proba_not_canceled),
            "probability_percent": round(proba_not_canceled * 100, 2),
            "threshold": self.threshold
        }
        
        return result


class InputPreprocessor:
    
    MEAL_PLAN_MAP = {
        "Breakfast Only": 0.0,
        "Breakfast + Dinner": 1.0,
        "All Meals": 3.0,
        "No Meal Plan": 0.0
    }
    
    MARKET_SEGMENT_MAP = {
        "Online": 4.0,
        "Offline": 3.0,
        "Corporate": 2.0,
        "Aviation": 1.0,
        "Complementary": 0.0
    }
    
    ROOM_TYPE_MAP = {
        "Room Type 1": 0.0,
        "Room Type 2": 1.0,
        "Room Type 3": 2.0,
        "Room Type 4": 3.0
    }
    
    @staticmethod
    def validate_and_encode(raw_input: Dict) -> Dict[str, float]:
        processed = {
            "lead_time": InputPreprocessor._safe_float(
                raw_input.get("lead_time"), "lead_time", min_val=0
            ),
            "no_of_special_requests": InputPreprocessor._safe_float(
                raw_input.get("no_of_special_requests"), 
                "no_of_special_requests", 
                min_val=0, 
                max_val=10
            ),
            "avg_price_per_room": InputPreprocessor._safe_float(
                raw_input.get("avg_price_per_room"), 
                "avg_price_per_room", 
                min_val=0
            ),
            "arrival_month": InputPreprocessor._safe_float(
                raw_input.get("arrival_month"), 
                "arrival_month", 
                min_val=1, 
                max_val=12
            ),
            "arrival_date": InputPreprocessor._safe_float(
                raw_input.get("arrival_date"), 
                "arrival_date", 
                min_val=1, 
                max_val=31
            ),
            "no_of_week_nights": InputPreprocessor._safe_float(
                raw_input.get("no_of_week_nights"), 
                "no_of_week_nights", 
                min_val=0
            ),
            "no_of_weekend_nights": InputPreprocessor._safe_float(
                raw_input.get("no_of_weekend_nights"), 
                "no_of_weekend_nights", 
                min_val=0
            ),
            "market_segment_type": InputPreprocessor._encode_categorical(
                raw_input.get("market_segment_type"),
                InputPreprocessor.MARKET_SEGMENT_MAP,
                "market_segment_type"
            ),
            "type_of_meal_plan": InputPreprocessor._encode_categorical(
                raw_input.get("type_of_meal_plan"),
                InputPreprocessor.MEAL_PLAN_MAP,
                "type_of_meal_plan"
            ),
            "room_type_reserved": InputPreprocessor._encode_categorical(
                raw_input.get("room_type_reserved"),
                InputPreprocessor.ROOM_TYPE_MAP,
                "room_type_reserved"
            )
        }
        
        return processed
    
    @staticmethod
    def _safe_float(value, field_name: str, min_val=None, max_val=None) -> float:
        try:
            num = float(value)
            
            if min_val is not None and num < min_val:
                raise ValueError(f"{field_name} must be >= {min_val}")
            if max_val is not None and num > max_val:
                raise ValueError(f"{field_name} must be <= {max_val}")
            
            return num
            
        except (ValueError, TypeError):
            raise ValueError(f"Invalid value for {field_name}: '{value}'. Must be a number.")
    
    @staticmethod
    def _encode_categorical(value, mapping: Dict, field_name: str) -> float:
        if value not in mapping:
            valid_values = list(mapping.keys())
            raise ValueError(f"Invalid {field_name}: '{value}'. Valid options: {valid_values}")
        return mapping[value]