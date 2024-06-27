# DO NOT EDIT: File is generated by code generator.

from pokepay.request.request import PokepayRequest
from pokepay.response.account_with_user import AccountWithUser


class CreateCustomerAccount(PokepayRequest):
    def __init__(self, private_money_id, **rest_args):
        self.path = "/accounts" + "/customers"
        self.method = "POST"
        self.body_params = {"private_money_id": private_money_id}
        self.body_params.update(rest_args)
        if 'start' in self.body_params:
            self.body_params['from'] = self.body_params.pop('start')
        self.response_class = AccountWithUser
