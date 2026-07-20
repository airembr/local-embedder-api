import warnings
from pathlib import Path
from typing import List, Tuple

import torch
from transformers import AutoTokenizer

from app.config import question_model_dir

_tokenizer = AutoTokenizer.from_pretrained(question_model_dir)
q_model_path = Path(question_model_dir) / "model_quantized.pt"

with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    _classifier = torch.load(q_model_path, weights_only=False)
_classifier.eval()

_MAX_LENGTH = 64


def get_questions(sentences: List[str]) -> List[Tuple[str, float]]:
    enc = _tokenizer(
        sentences,
        truncation=True,
        padding=True,
        max_length=_MAX_LENGTH,
        return_tensors="pt",
        return_token_type_ids=False,
    )
    with torch.no_grad():
        logits = _classifier(**enc).logits
    probs = torch.softmax(logits, dim=-1)
    scores, ids = probs.max(dim=-1)
    return [(_classifier.config.id2label[i.item()], s.item()) for i, s in zip(ids, scores)]
