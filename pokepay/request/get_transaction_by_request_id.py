# DO NOT EDIT: File is generated by code generator.

from pokepay.request.request import PokepayRequest
from pokepay.response.transaction_detail import TransactionDetail


class GetTransactionByRequestId(PokepayRequest):
    def __init__(self, request_id):
        self.path = "/transactions" + "/requests" + "/" + request_id
        self.method = "GET"
        self.body_params = {}
        
        self.response_class = TransactionDetail
