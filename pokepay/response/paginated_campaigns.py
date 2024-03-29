# DO NOT EDIT: File is generated by code generator.

from pokepay.response.response import PokepayResponse


class PaginatedCampaigns(PokepayResponse):
    def __init__(self, response, response_body):
        super().__init__(response, response_body)
        self.rows = response_body['rows']
        self.count = response_body['count']
        self.pagination = response_body['pagination']

    def rows(self):
        return self.rows

    def count(self):
        return self.count

    def pagination(self):
        return self.pagination

