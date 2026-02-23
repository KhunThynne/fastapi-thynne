# copied from https://github.com/prisma/prisma/blob/23d5ef0672372035a84552b6b457197ca19f486d/packages/client/src/runtime/core/engines/common/types/Metrics.ts
from __future__ import annotations

from typing import Generic, NamedTuple, TypeVar

from pydantic import BaseModel

from ._compat import GenericModel, model_rebuild

__all__ = (
    "Metrics",
    "Metric",
    "MetricHistogram",
)


_T = TypeVar("_T")


# TODO: check if int / float is right


class Metrics(BaseModel):
    counters: list[Metric[int]]
    gauges: list[Metric[float]]
    histograms: list[Metric[MetricHistogram]]


class Metric(GenericModel, Generic[_T]):
    key: str
    value: _T
    labels: dict[str, str]
    description: str


class MetricHistogram(BaseModel):
    sum: float
    count: int
    buckets: list[HistogramBucket]


class HistogramBucket(NamedTuple):
    max_value: float
    total_count: int


model_rebuild(Metric)
model_rebuild(Metrics)
model_rebuild(MetricHistogram)
