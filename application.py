import joblib
import numpy as np
from flask import Flask, render_template, request
from config.paths_config import MODEL_OUTPUT_PATH
import os

app = Flask(__name__)

artifact = joblib.load(MODEL_OUTPUT_PATH)

model = artifact["model"]
threshold = artifact["threshold"]
features = artifact["features"]
model_name = artifact["model_name"]

print(f"Loaded model: {model_name}")
print(f"Threshold  : {threshold}")

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

@app.route("/", methods=["GET", "POST"])
def index():
    prediction_result = None
    probability = None
    error_message = None

    if request.method == "POST":
        try:
            input_data = {
                "lead_time": float(request.form.get("lead_time", 0)),
                "no_of_special_requests": float(request.form.get("no_of_special_requests", 0)),
                "avg_price_per_room": float(request.form.get("avg_price_per_room", 0)),
                "market_segment_type": MARKET_SEGMENT_MAP.get(request.form.get("market_segment_type", ""), 0.0),
                "arrival_month": float(request.form.get("arrival_month", 1)),
                "arrival_date": float(request.form.get("arrival_date", 1)),
                "no_of_week_nights": float(request.form.get("no_of_week_nights", 0)),
                "no_of_weekend_nights": float(request.form.get("no_of_weekend_nights", 0)),
                "type_of_meal_plan": MEAL_PLAN_MAP.get(request.form.get("type_of_meal_plan", ""), 0.0),
                "room_type_reserved": ROOM_TYPE_MAP.get(request.form.get("room_type_reserved", ""), 0.0),
            }

            X = np.array([input_data[col] for col in features]).reshape(1, -1)

            proba_not_canceled = model.predict_proba(X)[0, 1]
            prediction = int(proba_not_canceled >= threshold)

            prediction_result = "Not Canceled" if prediction else "Canceled"
            probability = round(proba_not_canceled * 100, 2)

        except Exception as e:
            error_message = str(e)

    return render_template(
        "index.html",
        prediction=prediction_result,
        probability=probability,
        error=error_message
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
