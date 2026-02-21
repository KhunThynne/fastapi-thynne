import strawberry

from strawberry.fastapi import GraphQLRouter

from app.api.graphql.security import get_context

# Users
from app.api.graphql.users.mutations import UsersMutation
from app.api.graphql.users.queries import UsersQuery


@strawberry.type
class Query(UsersQuery):
    pass


@strawberry.type
class Mutation(UsersMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,  # type: ignore
)
