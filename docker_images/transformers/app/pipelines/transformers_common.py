import torch
from typing import Any, Dict
from app.pipelines import Pipeline
from transformers import pipeline
from huggingface_hub import model_info


class TransformersPipeline(Pipeline):
    def __init__(
        self,
        model_id: str,
    ):
        if torch.cuda.is_available():
            device = 0
        else:
            device = -1
        model_data = model_info(model_id)
        self.pipeline = pipeline(model=model_data.modelId, task=model_data.pipeline_tag, device=device)

    def __call__(self, inputs: Dict[str, str]) -> Dict[str, Any]:
        return self.pipeline(inputs)
