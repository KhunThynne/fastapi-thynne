from enum import Enum
from typing import Any, ClassVar, Union

from pydantic import BaseModel

from .._compat import (
    PYDANTIC_V2,
    ConfigDict,
    cached_property,
    model_rebuild,
    root_validator,
)
from .models import AnyData, DMMFEnumType, Model as ModelInfo, PrimaryKey, data_ctx
from .utils import to_constant_case


class Kind(str, Enum):
    alias = "alias"
    union = "union"
    typeddict = "typeddict"
    enum = "enum"


class PrismaType(BaseModel):
    name: str
    kind: Kind
    subtypes: list["PrismaType"] = []

    @classmethod
    def from_variants(
        cls, variants: list["PrismaType"], **kwargs: Any
    ) -> Union["PrismaUnion", "PrismaAlias"]:
        """Return either a `PrismaUnion` or a `PrismaAlias` depending on the number of variants"""
        if len(variants) > 1:
            return PrismaUnion(variants=variants, **kwargs)

        return PrismaAlias(subtypes=variants, **kwargs)


class PrismaDict(PrismaType):
    kind: Kind = Kind.typeddict
    fields: dict[str, str]
    total: bool


class PrismaUnion(PrismaType):
    kind: Kind = Kind.union
    variants: list[PrismaType]

    @root_validator(pre=True)
    @classmethod
    def add_subtypes(cls, values: dict[str, Any]) -> dict[str, Any]:
        # add all variants as subtypes so that we don't have to special
        # case rendering subtypes for unions
        if "variants" in values:
            subtypes = values.get("subtypes", [])
            subtypes.extend(values["variants"])
            values["subtypes"] = subtypes
        return values


class PrismaEnum(PrismaType):
    kind: Kind = Kind.enum
    members: list[tuple[str, str]]


class PrismaAlias(PrismaType):
    kind: Kind = Kind.alias
    to: str

    @root_validator(pre=True)
    @classmethod
    def transform_to(cls, values: dict[str, Any]) -> dict[str, Any]:
        if "to" not in values and "subtypes" in values:
            values["to"] = values["subtypes"][0].name
        return values


class Schema(BaseModel):
    models: list["Model"]

    @classmethod
    def from_data(cls, data: AnyData) -> "Schema":
        models = [Model(info=model) for model in data.dmmf.datamodel.models]
        return cls(models=models)

    def get_model(self, name: str) -> "Model":
        for model in self.models:
            if model.info.name == name:
                return model

        raise LookupError(f"Unknown model: {name}")


class Model(BaseModel):
    info: ModelInfo

    if PYDANTIC_V2:
        model_config: ClassVar[ConfigDict] = ConfigDict(
            ignored_types=(cached_property,)
        )
    else:

        class Config:
            keep_untouched: tuple[type[Any], ...] = (cached_property,)

    @cached_property
    def where_unique(self) -> PrismaType:
        info = self.info
        model = info.name
        variants: list[PrismaType] = [
            PrismaDict(
                total=True,
                name=f"_{model}WhereUnique_{field.name}_Input",
                fields={
                    field.name: field.python_type,
                },
            )
            for field in info.scalar_fields
            if field.is_id or field.is_unique
        ]

        for key in [info.compound_primary_key, *info.unique_indexes]:
            if key is None:
                continue

            if isinstance(key, PrimaryKey):
                name = f"_{model}CompoundPrimaryKey"
            else:
                name = f"_{model}Compound{key.name}Key"

            variants.append(
                PrismaDict(
                    name=name,
                    total=True,
                    fields={
                        key.name: f"{name}Inner",
                    },
                    subtypes=[
                        PrismaDict(
                            total=True,
                            name=f"{name}Inner",
                            fields={
                                field.name: field.python_type
                                for field in map(info.resolve_field, key.fields)
                            },
                        )
                    ],
                )
            )

        return PrismaType.from_variants(variants, name=f"{model}WhereUniqueInput")

    @cached_property
    def order_by(self) -> PrismaType:
        model = self.info.name
        variants: list[PrismaType] = [
            PrismaDict(
                name=f"_{model}_{field.name}_OrderByInput",
                total=True,
                fields={
                    field.name: "SortOrder",
                },
            )
            for field in self.info.scalar_fields
        ]
        # Full-text search relevance sorting
        if data_ctx.get().datasources[0].active_provider in {"postgresql", "mysql"}:
            relevance_type = PrismaDict(
                name=f"_{model}_RelevanceOrderByInput",
                total=True,
                fields={
                    "_relevance": f"_{model}_RelevanceInner",
                },
                subtypes=[
                    PrismaDict(
                        name=f"_{model}_RelevanceInner",
                        total=True,
                        fields={
                            "fields": f"List[{model}ScalarFieldKeys]",
                            "search": "str",
                            "sort": "SortOrder",
                        },
                    )
                ],
            )
            variants.append(relevance_type)
        return PrismaType.from_variants(variants, name=f"{model}OrderByInput")


class ClientTypes(BaseModel):
    transaction_isolation_level: PrismaEnum | None

    @classmethod
    def from_data(cls, data: AnyData) -> "ClientTypes":
        enum_types = data.dmmf.prisma_schema.enum_types.prisma

        return cls(
            transaction_isolation_level=construct_enum_type(
                enum_types, name="TransactionIsolationLevel"
            ),
        )


def construct_enum_type(
    dmmf_enum_types: list[DMMFEnumType], *, name: str
) -> PrismaEnum | None:
    enum_type = next((t for t in dmmf_enum_types if t.name == name), None)
    if not enum_type:
        return None

    return PrismaEnum(
        name=name,
        members=[
            (to_constant_case(str(value)), str(value)) for value in enum_type.values
        ],
    )


model_rebuild(Schema)
model_rebuild(PrismaType)
model_rebuild(PrismaDict)
model_rebuild(PrismaAlias)
