from pydantic import BaseModel
from pipeline.constants import *


class PayloadSchemaGenerator:
    def __init__(self, request_json: dict):
        self.data = request_json
        self.payload_schema = {TEXT: self.data.get(TEXT, "")}

    def create_payload_schema(self):
        return PayloadSchema(**self.payload_schema)


class PayloadSchema(BaseModel):
    text: str
