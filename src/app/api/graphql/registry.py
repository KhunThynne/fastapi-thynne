from .licenses.mutations import LicenseMutation
from .licenses.queries import LicenseQuery
from .product.mutations import ProductMutation
from .product.queries import ProductQuery


class QueryRegistry(LicenseQuery, ProductQuery):
    pass


class MutationRegistry(LicenseMutation, ProductMutation):
    pass
