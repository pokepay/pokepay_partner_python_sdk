from pokepay.response.response import PokepayResponse


class PokepayRequest(object):
    def __init__(self):
        self.path = '/'
        self.method = 'GET'
        self.body_params = {}
        self.response_class = PokepayResponse

    def path(self):
        return self.path

    def method(self):
        return self.method

    def body_params(self):
        return self.body_params

    def response_class(self):
        return self.response_class
