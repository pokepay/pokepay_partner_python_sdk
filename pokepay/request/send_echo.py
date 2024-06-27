# DO NOT EDIT: File is generated by code generator.

from pokepay.request.request import PokepayRequest
from pokepay.response.echo import Echo


class SendEcho(PokepayRequest):
    def __init__(self, message):
        self.path = "/echo"
        self.method = "POST"
        self.body_params = {"message": message}
        
        if 'start' in self.body_params:
            self.body_params['from'] = self.body_params.pop('start')
        self.response_class = Echo
