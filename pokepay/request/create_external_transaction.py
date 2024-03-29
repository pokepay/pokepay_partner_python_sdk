# DO NOT EDIT: File is generated by code generator.

from pokepay.request.request import PokepayRequest
from pokepay.response.external_transaction import ExternalTransaction


class CreateExternalTransaction(PokepayRequest):
    def __init__(self, shop_id, customer_id, private_money_id, amount, **rest_args):
        self.path = "/external-transactions"
        self.method = "POST"
        self.body_params = {"shop_id": shop_id,
                            "customer_id": customer_id,
                            "private_money_id": private_money_id,
                            "amount": amount}
        self.body_params.update(rest_args)
        self.response_class = ExternalTransaction
