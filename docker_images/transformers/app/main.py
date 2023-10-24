import functools
import logging
import os
from typing import Dict, Type

from api_inference_community.routes import pipeline_route, status_ok
from app.pipelines import TransformersPipeline, Pipeline
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from api_example import image_to_text_example, asr_example, text_speech_example

TASK = os.getenv("TASK")
MODEL_ID = os.getenv("MODEL_ID")


logger = logging.getLogger(__name__)


# Add the allowed tasks
# Supported tasks are:
# - text-generation
# - text-classification
# - token-classification
# - translation
# - summarization
# - automatic-speech-recognition
# - ...
# For instance
# from app.pipelines import AutomaticSpeechRecognitionPipeline
# ALLOWED_TASKS = {"automatic-speech-recognition": AutomaticSpeechRecognitionPipeline}
# You can check the requirements and expectations of each pipelines in their respective
# directories. Implement directly within the directories.
ALLOWED_TASKS: Dict[str, Type[Pipeline]] = {
    "text-classification": TransformersPipeline,
    "audio-classification": TransformersPipeline,
    "automatic-speech-recognition": TransformersPipeline,
    "image-to-text": TransformersPipeline,
    "text-to-speech": TransformersPipeline,
}

templates = Jinja2Templates(directory='app/templates')


async def homepage(request):
    task = os.environ['TASK']
    api_url = 'https://' + os.environ['result_url']

    if task == 'image-to-text':
        result = image_to_text_example(api_url)
    elif task == 'automatic-speech-recognition':
        result = asr_example(api_url)
    elif task == 'text-to-speech':
        result = text_speech_example(api_url)

    context = {'request': request, 'api_url': api_url, 'python_code': result[0],
               'javaScript_code': result[1], 'curl_code': result[2]}
    return templates.TemplateResponse('index.html', context)


@functools.lru_cache()
def get_pipeline() -> Pipeline:
    task = os.environ["TASK"]
    model_id = os.environ["MODEL_ID"]
    if task not in ALLOWED_TASKS:
        raise EnvironmentError(f"{task} is not a valid pipeline for model : {model_id}")
    return ALLOWED_TASKS[task](model_id)


routes = [
    Mount('/static', app=StaticFiles(directory="app/templates/static"), name="static"),
    Route('/', endpoint=homepage),
    Route("/{whatever:path}", status_ok),
    Route("/{whatever:path}", pipeline_route, methods=["POST"]),
]

middleware = [Middleware(GZipMiddleware, minimum_size=1000)]
if os.environ.get("DEBUG", "") == "1":
    from starlette.middleware.cors import CORSMiddleware

    middleware.append(
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_headers=["*"],
            allow_methods=["*"],
        )
    )

app = Starlette(routes=routes, middleware=middleware)


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.handlers = [handler]

    # Link between `api-inference-community` and framework code.
    app.get_pipeline = get_pipeline
    try:
        get_pipeline()
    except Exception:
        # We can fail so we can show exception later.
        pass


if __name__ == "__main__":
    try:
        get_pipeline()
    except Exception:
        # We can fail so we can show exception later.
        pass
