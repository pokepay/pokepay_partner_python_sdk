# DO NOT EDIT: File is generated by code generator.

from pokepay.response.response import PokepayResponse


class OrganizationSummary(PokepayResponse):
    def __init__(self, response, response_body):
        super().__init__(response, response_body)
        self.count = response_body['count']
        self.money_amount = response_body['money_amount']
        self.money_count = response_body['money_count']
        self.point_amount = response_body['point_amount']
        self.raw_point_amount = response_body['raw_point_amount']
        self.campaign_point_amount = response_body['campaign_point_amount']
        self.point_count = response_body['point_count']

    def count(self):
        return self.count

    def money_amount(self):
        return self.money_amount

    def money_count(self):
        return self.money_count

    def point_amount(self):
        return self.point_amount

    def raw_point_amount(self):
        return self.raw_point_amount

    def campaign_point_amount(self):
        return self.campaign_point_amount

    def point_count(self):
        return self.point_count

