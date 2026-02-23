from .accounts.mutations import AccountsMutation
from .accounts.queries import AccountsQuery
from .users.mutations import UserMutation
from .users.queries import UserQuery


class QueryRegistry(UserQuery, AccountsQuery):
    pass


class MutationRegistry(UserMutation, AccountsMutation):
    pass
