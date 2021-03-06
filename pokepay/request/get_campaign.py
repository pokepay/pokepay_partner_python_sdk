# DO NOT EDIT: File is generated by code generator.

from pokepay_partner_python_sdk.pokepay.request.request import PokepayRequest
from pokepay_partner_python_sdk.pokepay.response.campaign import Campaign


class GetCampaign(PokepayRequest):
    def __init__(self, campaign_id):
        self.path = "/campaigns" + "/" + campaign_id
        self.method = "GET"
        self.body_params = {}
        
        self.response_class = Campaign
