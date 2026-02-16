import strawberry

from app.api.graphql.users.types import UserType


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def create_user(self, username: str, email: str) -> UserType:
        # Mock implementation
        return UserType(id=3, username=username, email=email)
