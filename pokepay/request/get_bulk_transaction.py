# DO NOT EDIT: File is generated by code generator.

from pokepay_partner_python_sdk.pokepay.request.request import PokepayRequest
from pokepay_partner_python_sdk.pokepay.response.bulk_transaction import BulkTransaction


class GetBulkTransaction(PokepayRequest):
    def __init__(self, bulk_transaction_id):
        self.path = "/bulk-transactions" + "/" + bulk_transaction_id
        self.method = "GET"
        self.body_params = {}
        
        self.response_class = BulkTransaction
