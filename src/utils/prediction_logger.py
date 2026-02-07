import json
from datetime import datetime
from pathlib import Path


class PredictionLogger:
    
    def __init__(self, log_dir: str = "logs/predictions"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def log_prediction(self, input_data: dict, result: dict, source: str = "web"):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "input": input_data,
            "output": result
        }
        
        log_file = self.log_dir / f"predictions_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')


prediction_logger = PredictionLogger()