import os
from typing import Any, Dict

from app.pipelines import Pipeline
from transformers import pipeline
from huggingface_hub import model_info


class ImageToTextPipeline(Pipeline):
    def __init__(
        self,
        model_id: str,
    ):
        use_auth_token = os.getenv("HF_API_TOKEN")
        model_data = model_info(model_id, token=use_auth_token)
        task_type = model_data.pipeline_tag
        self.ldm = pipeline(model=model_id, task=task_type)

    def __call__(self, inputs: Dict[str, str]) -> Dict[str, Any]:
        return self.ldm(inputs)
