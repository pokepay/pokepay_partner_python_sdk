# DO NOT EDIT: File is generated by code generator.

from pokepay_partner_python_sdk.pokepay.request.request import PokepayRequest
from pokepay_partner_python_sdk.pokepay.response.transaction import Transaction


class GetTransaction(PokepayRequest):
    def __init__(self, transaction_id):
        self.path = "/transactions" + "/" + transaction_id
        self.method = "GET"
        self.body_params = {}
        
        self.response_class = Transaction