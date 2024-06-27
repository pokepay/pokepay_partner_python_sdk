# DO NOT EDIT: File is generated by code generator.

from pokepay.request.request import PokepayRequest
from pokepay.response.bank_registering_info import BankRegisteringInfo


class CreateBank(PokepayRequest):
    def __init__(self, user_device_id, private_money_id, callback_url, kana, **rest_args):
        self.path = "/user-devices" + "/" + user_device_id + "/banks"
        self.method = "POST"
        self.body_params = {"private_money_id": private_money_id,
                            "callback_url": callback_url,
                            "kana": kana}
        self.body_params.update(rest_args)
        if 'start' in self.body_params:
            self.body_params['from'] = self.body_params.pop('start')
        self.response_class = BankRegisteringInfo
