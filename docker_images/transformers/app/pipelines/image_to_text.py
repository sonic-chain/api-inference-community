from typing import Any, Dict

from app.pipelines import Pipeline
from transformers import (
    ImageToTextPipeline as TransformersImageToTextPipeline,
)


class ImageToTextPipeline(Pipeline):
    def __init__(
        self,
        model_id: str,
    ):
        self.pipeline = self._load_pipeline_instance(TransformersImageToTextPipeline, model_id)

    def __call__(self, inputs: Dict[str, str]) -> Dict[str, Any]:
        return self.pipeline(inputs)
