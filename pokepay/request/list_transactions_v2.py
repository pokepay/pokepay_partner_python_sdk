# DO NOT EDIT: File is generated by code generator.

from pokepay.request.request import PokepayRequest
from pokepay.response.paginated_transaction_v2 import PaginatedTransactionV2


class ListTransactionsV2(PokepayRequest):
    def __init__(self, **rest_args):
        self.path = "/transactions-v2"
        self.method = "GET"
        self.body_params = {}
        self.body_params.update(rest_args)
        self.response_class = PaginatedTransactionV2
