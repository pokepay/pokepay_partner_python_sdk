# DO NOT EDIT: File is generated by code generator.

from pokepay.request.request import PokepayRequest
from pokepay.response.pong import Pong


class GetPing(PokepayRequest):
    def __init__(self, ):
        self.path = "/ping"
        self.method = "GET"
        self.body_params = {}
        
        self.response_class = Pong
