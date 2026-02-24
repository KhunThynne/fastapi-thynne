import strawberry

from strawberry.fastapi import GraphQLRouter

from app.api.graphql.registry import MutationRegistry, QueryRegistry
from app.api.graphql.security import get_context


@strawberry.type
class Query(QueryRegistry):
    @strawberry.field
    def health(self) -> str:
        return "ok"


@strawberry.type
class Mutation(MutationRegistry):
    @strawberry.mutation
    def ping(self) -> str:
        return "pong"


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,  # type: ignore
)
