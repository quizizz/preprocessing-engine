import os

from sanic.log import logger

from pipeline.runner import PipelineRunner
from structures.dto import DTO


async def init(app):
    pipeline_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "pipeline_config.yaml")
    pipeline_runner = PipelineRunner(pipeline_path)
    app.ctx.pipeline_runner = pipeline_runner
    logger.info("Pipeline runner instantiated")
    try:
        assert isinstance(await pipeline_runner.run(DTO({"text": "Dummy teXts'' the"})), dict)
    except Exception as e:
        raise Exception(f"Warm up pipeline failed: {e}")
