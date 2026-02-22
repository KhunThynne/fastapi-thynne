from models.account import AccountType
from repository.account_repo import AccountRepository

from ..factory import strawberry_crud

account_repo = AccountRepository()


@strawberry_crud(gql_type=AccountType, repo=account_repo)
class AccountsQuery:
    # ได้ get_accounts() และ get_account() มาใช้ทันที
    pass
