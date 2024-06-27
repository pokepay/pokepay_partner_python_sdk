# DO NOT EDIT: File is generated by code generator.

from pokepay.request.request import PokepayRequest
from pokepay.response.account_detail import AccountDetail


class CreateUserAccount(PokepayRequest):
    def __init__(self, user_id, private_money_id, **rest_args):
        self.path = "/users" + "/" + user_id + "/accounts"
        self.method = "POST"
        self.body_params = {"private_money_id": private_money_id}
        self.body_params.update(rest_args)
        if 'start' in self.body_params:
            self.body_params['from'] = self.body_params.pop('start')
        self.response_class = AccountDetail
