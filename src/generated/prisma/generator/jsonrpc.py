from __future__ import annotations

import json
import logging
import sys

from pathlib import Path
from typing import Any, Literal, Union

from pydantic import Field
from typing_extensions import TypedDict

from .._compat import model_json
from .models import BaseModel

log: logging.Logger = logging.getLogger(__name__)


__all__ = ("Manifest",)


class Request(BaseModel):
    # JSON RPC protocol version
    jsonrpc: str = "2.0"

    # identifies a request
    id: int

    # request intention
    method: str

    # request payload
    params: dict[str, Any] | None = None


class SuccessResponse(BaseModel):
    id: int
    jsonrpc: str = "2.0"
    result: dict[str, Any] | None = None


class ErrorData(TypedDict):
    code: int
    message: str
    data: object


class ErrorResponse(BaseModel):
    id: int
    error: ErrorData
    jsonrpc: str = "2.0"


Response = Union[SuccessResponse, ErrorResponse]

EngineType = Literal[
    "prismaFmt",
    "queryEngine",
    "libqueryEngine",
    "migrationEngine",
    "introspectionEngine",
]


class Manifest(BaseModel):
    """Generator metadata"""

    prettyName: str = Field(alias="name")
    defaultOutput: str | Path = Field(alias="default_output")
    denylist: list[str] | None = None
    requiresEngines: list[EngineType] | None = Field(
        alias="requires_engines", default=None
    )
    requiresGenerators: list[str] | None = Field(
        alias="requires_generators", default=None
    )


# TODO: proper types
method_mapping: dict[str, type[Request]] = {
    "getManifest": Request,
    "generate": Request,
}


def readline() -> str | None:
    try:
        line = input()
    except EOFError:
        log.debug("Ignoring EOFError")
        return None

    return line


def parse(line: str) -> Request:
    log.debug("Parsing JSONRPC request line %s", line)

    data = json.loads(line)
    try:
        method = data["method"]
    except (KeyError, TypeError):
        # TODO
        raise
    else:
        request_type = method_mapping.get(method)
        if request_type is None:
            raise RuntimeError(f"Unknown method: {method}")

    return request_type(**data)


def reply(response: Response) -> None:
    dumped = model_json(response) + "\n"
    print(dumped, file=sys.stderr, flush=True)  # noqa: T201
    log.debug("Replied with %s", dumped)
