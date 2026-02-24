from modules.product.model import ProductType
from modules.product.repository import ProductRepository

from ..factory import strawberry_crud


@strawberry_crud(mode="query", gql_type=ProductType, repo=ProductRepository())
class ProductQuery:
    pass
