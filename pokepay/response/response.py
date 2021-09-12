class PokepayResponse(object):
    def __init__(self, response, response_body):
        self.body = response_body
        self.elapsed = response.elapsed
        self.status_code = response.status_code
        self.ok = response.ok
        self.headers = response.headers
        self.url = response.url

    def body(self):
        return self.body

    def elapsed(self):
        return self.elapsed

    def status_code(self):
        return self.status_code

    def ok(self):
        return self.ok

    def headers(self):
        return self.headers

    def url(self):
        return self.url
