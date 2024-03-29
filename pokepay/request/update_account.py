# DO NOT EDIT: File is generated by code generator.

from pokepay.request.request import PokepayRequest
from pokepay.response.account_detail import AccountDetail


class UpdateAccount(PokepayRequest):
    def __init__(self, account_id, **rest_args):
        self.path = "/accounts" + "/" + account_id
        self.method = "PATCH"
        self.body_params = {}
        self.body_params.update(rest_args)
        self.response_class = AccountDetail
