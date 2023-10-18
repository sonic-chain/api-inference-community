from abc import ABC, abstractmethod
from typing import Any
from huggingface_hub import hf_hub_download, model_info

class Pipeline(ABC):
    @abstractmethod
    def __init__(self, model_id: str):
        raise NotImplementedError("Pipelines should implement an __init__ method")

    @abstractmethod
    def __call__(self, inputs: Any) -> Any:
        raise NotImplementedError("Pipelines should implement a __call__ method")

    @staticmethod
    def _load_pipeline_instance(pipeline_class, model_id):
        model_data = model_info(model_id)
        return pipeline_class(model=model_data.modelId, task=model_data.pipeline_tag)


class PipelineException(Exception):
    pass
