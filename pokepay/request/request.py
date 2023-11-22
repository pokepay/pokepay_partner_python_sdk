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
        # convert key 'start' to 'from' because of python's reserved word
        if 'start' not in self.body_params:
            return self.body_params

        output_dict = self.body_params.copy()
        output_dict['from'] = output_dict['start']
        del output_dict['start']

        return output_dict

    def response_class(self):
        return self.response_class
