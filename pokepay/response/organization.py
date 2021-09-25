# DO NOT EDIT: File is generated by code generator.

from pokepay_partner_python_sdk.pokepay.response.response import PokepayResponse


class Organization(PokepayResponse):
    def __init__(self, response, response_body):
        super().__init__(response, response_body)
        self.code = response_body['code']
        self.name = response_body['name']

    def code(self):
        return self.code

    def name(self):
        return self.name
