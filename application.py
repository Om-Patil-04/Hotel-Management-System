import os
import warnings
from flask import Flask, render_template, request, jsonify
from pydantic import ValidationError
from src.pipeline.predict_pipeline import PredictPipeline, InputPreprocessor
from src.utils.prediction_logger import prediction_logger
from src.schemas.input_schema import BookingInput

warnings.filterwarnings("ignore", message=".*development server.*")

app = Flask(__name__)

pipeline = PredictPipeline()


@app.route("/", methods=["GET", "POST"])
def index():
    prediction_result = None
    probability = None
    error_message = None

    if request.method == "POST":
        try:
            processed_input = InputPreprocessor.validate_and_encode(request.form.to_dict())
            result = pipeline.predict(processed_input)
            
            prediction_result = result["prediction"]
            probability = result["probability_percent"]
            
            prediction_logger.log_prediction(request.form.to_dict(), result, source="web")
            
        except ValueError as e:
            error_message = f"Validation Error: {str(e)}"
            
        except Exception as e:
            error_message = f"Prediction Error: {str(e)}"

    return render_template(
        "index.html",
        prediction=prediction_result,
        probability=probability,
        error=error_message
    )


@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        booking_input = BookingInput(**request.json)
        raw_dict = booking_input.dict()
        processed_input = InputPreprocessor.validate_and_encode(raw_dict)
        result = pipeline.predict(processed_input)
        
        prediction_logger.log_prediction(raw_dict, result, source="api")
        
        return jsonify({
            "success": True,
            "data": result
        }), 200
        
    except ValidationError as e:
        return jsonify({
            "success": False,
            "error": "Validation error",
            "details": e.errors()
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "details": str(e)
        }), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model": pipeline.model_name,
        "threshold": pipeline.threshold,
        "features": pipeline.features
    }), 200


@app.route("/api/info", methods=["GET"])
def model_info():
    return jsonify({
        "model_name": pipeline.model_name,
        "threshold": pipeline.threshold,
        "features": pipeline.features,
        "has_encoders": pipeline.encoders is not None,
        "has_scaler": pipeline.scaler is not None
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("DEBUG", "False").lower() == "true"
    
    print(f"\nStarting Hotel Booking Prediction Service")
    print(f"Model: {pipeline.model_name}")
    print(f"Threshold: {pipeline.threshold}")
    print(f"Server: http://127.0.0.1:{port}\n")
    
    app.run(host="0.0.0.0", port=port, debug=debug)