from app.api.graphql.factory import strawberry_crud
from modules.user.model import UserType
from modules.user.repository import UserRepository

user_repo = UserRepository()


@strawberry_crud(mode="query", gql_type=UserType, repo=user_repo)
class UserQuery:
    pass
