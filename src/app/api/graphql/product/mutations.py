from app.api.graphql.factory import strawberry_crud
from modules.product.model import ProductType
from modules.product.repository import ProductRepository


@strawberry_crud(mode="mutation", gql_type=ProductType, repo=ProductRepository())
class ProductMutation:
    pass
