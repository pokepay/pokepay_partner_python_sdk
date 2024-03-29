# DO NOT EDIT: File is generated by code generator.

from pokepay.response.response import PokepayResponse


class PrivateMoneyOrganizationSummary(PokepayResponse):
    def __init__(self, response, response_body):
        super().__init__(response, response_body)
        self.organization_code = response_body['organization_code']
        self.topup = response_body['topup']
        self.payment = response_body['payment']

    def organization_code(self):
        return self.organization_code

    def topup(self):
        return self.topup

    def payment(self):
        return self.payment

