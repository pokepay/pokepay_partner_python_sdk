from pokepay.response.response import PokepayResponse


class Echo(PokepayResponse):
    def __init__(self, response, response_body):
        super().__init__(response, response_body)
        self.status = response_body['status']
        self.message = response_body['message']

    def status(self):
        return self.status

    def message(self):
        return self.message
