# DO NOT EDIT: File is generated by code generator.

from pokepay.request.request import PokepayRequest
from pokepay.response.organization_worker_task_webhook import OrganizationWorkerTaskWebhook


class CreateWebhook(PokepayRequest):
    def __init__(self, task, url):
        self.path = "/webhooks"
        self.method = "POST"
        self.body_params = {"task": task,
                            "url": url}
        
        if 'start' in self.body_params:
            self.body_params['from'] = self.body_params.pop('start')
        self.response_class = OrganizationWorkerTaskWebhook