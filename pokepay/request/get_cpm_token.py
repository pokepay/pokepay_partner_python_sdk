# DO NOT EDIT: File is generated by code generator.

from pokepay.request.request import PokepayRequest
from pokepay.response.cpm_token import CpmToken


class GetCpmToken(PokepayRequest):
    def __init__(self, cpm_token):
        self.path = "/cpm" + "/" + cpm_token
        self.method = "GET"
        self.body_params = {}
        
        if 'start' in self.body_params:
            self.body_params['from'] = self.body_params.pop('start')
        self.response_class = CpmToken
