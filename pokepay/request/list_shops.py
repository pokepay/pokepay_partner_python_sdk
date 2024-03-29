# DO NOT EDIT: File is generated by code generator.

from pokepay.request.request import PokepayRequest
from pokepay.response.paginated_shops import PaginatedShops


class ListShops(PokepayRequest):
    def __init__(self, **rest_args):
        self.path = "/shops"
        self.method = "GET"
        self.body_params = {}
        self.body_params.update(rest_args)
        self.response_class = PaginatedShops
