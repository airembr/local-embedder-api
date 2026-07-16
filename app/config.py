import os
from pathlib import Path

model = os.environ.get("EMBEDDING_MODEL", 'intfloat/multilingual-e5-base')  #768

question_model_dir = os.environ.get(
    "QUESTION_MODEL_DIR",
    str(Path(__file__).parent / "model" / "question_classifier_qat_quantized"),
)
question_model_name = "distilbert-question-classifier-qat-int8"
