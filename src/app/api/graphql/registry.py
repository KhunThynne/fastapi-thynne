from .licenses.mutations import LicenseMutation
from .licenses.queries import LicenseQuery


class QueryRegistry(LicenseQuery):
    pass


class MutationRegistry(LicenseMutation):
    pass
