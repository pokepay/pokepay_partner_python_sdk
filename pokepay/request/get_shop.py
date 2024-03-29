# DO NOT EDIT: File is generated by code generator.

from pokepay.request.request import PokepayRequest
from pokepay.response.shop_with_accounts import ShopWithAccounts


class GetShop(PokepayRequest):
    def __init__(self, shop_id):
        self.path = "/shops" + "/" + shop_id
        self.method = "GET"
        self.body_params = {}
        
        self.response_class = ShopWithAccounts
