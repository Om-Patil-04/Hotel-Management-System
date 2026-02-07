from pydantic import BaseModel, Field
from typing import Literal


class BookingInput(BaseModel):
    
    lead_time: float = Field(..., ge=0, description="Days between booking and arrival")
    no_of_special_requests: float = Field(..., ge=0, le=10, description="Number of special requests")
    avg_price_per_room: float = Field(..., ge=0, description="Average price per room")
    market_segment_type: Literal["Online", "Offline", "Corporate", "Aviation", "Complementary"]
    arrival_month: int = Field(..., ge=1, le=12)
    arrival_date: int = Field(..., ge=1, le=31)
    no_of_week_nights: float = Field(..., ge=0)
    no_of_weekend_nights: float = Field(..., ge=0)
    type_of_meal_plan: Literal["Breakfast Only", "Breakfast + Dinner", "All Meals", "No Meal Plan"]
    room_type_reserved: Literal["Room Type 1", "Room Type 2", "Room Type 3", "Room Type 4"]
    
    class Config:
        json_schema_extra = {
            "example": {
                "lead_time": 120.0,
                "no_of_special_requests": 2.0,
                "avg_price_per_room": 85.0,
                "market_segment_type": "Online",
                "arrival_month": 6,
                "arrival_date": 15,
                "no_of_week_nights": 2.0,
                "no_of_weekend_nights": 1.0,
                "type_of_meal_plan": "Breakfast Only",
                "room_type_reserved": "Room Type 1"
            }
        }