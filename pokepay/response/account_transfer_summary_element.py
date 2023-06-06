# DO NOT EDIT: File is generated by code generator.

from pokepay.response.response import PokepayResponse


class AccountTransferSummaryElement(PokepayResponse):
    def __init__(self, response, response_body):
        super().__init__(response, response_body)
        self.transfer_type = response_body['transfer_type']
        self.money_amount = response_body['money_amount']
        self.point_amount = response_body['point_amount']
        self.count = response_body['count']

    def transfer_type(self):
        return self.transfer_type

    def money_amount(self):
        return self.money_amount

    def point_amount(self):
        return self.point_amount

    def count(self):
        return self.count
