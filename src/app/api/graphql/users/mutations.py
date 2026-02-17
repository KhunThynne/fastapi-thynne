import strawberry

from app.models.user_schema import UserType


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def create_user(self, username: str, email: str) -> UserType:
        # Mock implementation
        return UserType(id=3, username=username, email=email)
