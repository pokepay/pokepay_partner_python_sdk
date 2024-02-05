# DO NOT EDIT: File is generated by code generator.

from pokepay.request.request import PokepayRequest
from pokepay.response.cashtray_with_result import CashtrayWithResult


class GetCashtray(PokepayRequest):
    def __init__(self, cashtray_id):
        self.path = "/cashtrays" + "/" + cashtray_id
        self.method = "GET"
        self.body_params = {}
        
        if 'start' in self.body_params:
            self.body_params['from'] = self.body_params.pop('start')
        self.response_class = CashtrayWithResult
