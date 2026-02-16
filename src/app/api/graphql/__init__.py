import strawberry

from app.api.graphql.users.mutations import UserMutation
from app.api.graphql.users.queries import UserQuery
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Query(UserQuery):
    pass


@strawberry.type
class Mutation(UserMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
