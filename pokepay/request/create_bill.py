# DO NOT EDIT: File is generated by code generator.

from pokepay.request.request import PokepayRequest
from pokepay.response.bill import Bill


class CreateBill(PokepayRequest):
    def __init__(self, private_money_id, shop_id, **rest_args):
        self.path = "/bills"
        self.method = "POST"
        self.body_params = {"private_money_id": private_money_id,
                            "shop_id": shop_id}
        self.body_params.update(rest_args)
        self.response_class = Bill
