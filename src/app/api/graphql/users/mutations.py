from app.api.graphql.factory import strawberry_crud
from modules.user.model import UserCreateInput, UserType
from modules.user.repository import UserRepository

user_repo = UserRepository()


@strawberry_crud(
    mode="mutation",
    gql_type=UserType,
    repo=user_repo,
    input_fields=UserCreateInput,
)
class UserMutation:
    pass
