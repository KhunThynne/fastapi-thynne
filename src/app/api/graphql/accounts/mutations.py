from app.api.graphql.factory import strawberry_crud
from modules.account.model import AccountType
from modules.account.repository import AccountRepository

account_repo = AccountRepository()


@strawberry_crud(mode="mutation", gql_type=AccountType, repo=account_repo)
class AccountsMutation:
    pass
