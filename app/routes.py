import time

from sanic import exceptions
from sanic.log import logger
from sanic.response import json
from sanic.views import HTTPMethodView

from structures.dto import DTO
from structures.payload_schema import PayloadSchema


class ProcessPayloadView(HTTPMethodView):
    @staticmethod
    def validata_schema(data: dict):
        if not data:
            raise Exception("Empty payload")
        if not isinstance(data, dict):
            raise Exception("Invalid schema")
        return data

    async def post(self, request):
        try:
            start = time.monotonic()
            data = self.validata_schema(request.json)
            logger.info(f"Processing request at /process: {request.json}")
            pipeline_runner = request.app.ctx.pipeline_runner
            response = await pipeline_runner.run(DTO(data))
            logger.info(
                f"Payload processed successfully: {response},"
                f" Processing time: {(time.monotonic() - start) * 1000:0.3f} ms"
            )
            return json(response)
        except exceptions.SanicException as e:
            logger.error(f"Sanic exception in payload processing: {e}")
            return json({'error': str(e)}, status=e.status_code)
        except Exception as e:
            logger.error(f"Error processing payload: {e}")
            return json({'error': 'Error processing payload'}, status=500)


class HealthCheckView(HTTPMethodView):

    async def get(self, request):
        return json({'status': 'healthy'})


def setup_routes(app):
    app.add_route(ProcessPayloadView.as_view(), '/process')
    app.add_route(HealthCheckView.as_view(), '/health')
