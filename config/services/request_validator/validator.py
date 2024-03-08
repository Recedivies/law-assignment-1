from typing import Any

from jsonschema import ValidationError, validate

from commons.exceptions import BadRequestException
from commons.patterns.runnable import Runnable
from plugins.constants import CONFIG_TYPE


class RequestBodyValidatorService(Runnable):
    @classmethod
    def run(cls, config: CONFIG_TYPE, **kwargs: Any) -> None:
        body_schema = config.get("body_schema", None)
        request_body = kwargs.get("request_body", None)

        required_properties = []
        schema_properties = {}
        for item in body_schema:
            for key, value in item.items():
                schema_properties[key] = {"type": value["type"]}

                if value.get("items", None):
                    schema_properties[key]["items"] = value.get("items")

                if "required" in value and value["required"]:
                    required_properties.append(key)

        schema = {
            "type": "object",
            "properties": schema_properties,
            "required": required_properties,
        }

        try:
            validate(instance=request_body, schema=schema)
        except ValidationError as e:
            raise BadRequestException(e.message)
