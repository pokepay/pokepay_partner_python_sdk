# DO NOT EDIT: File is generated by code generator.

from pokepay.response.response import PokepayResponse


class BulkTransactionJob(PokepayResponse):
    def __init__(self, response, response_body):
        super().__init__(response, response_body)
        self.id = response_body['id']
        self.bulk_transaction = response_body['bulk_transaction']
        self.type = response_body['type']
        self.sender_account_id = response_body['sender_account_id']
        self.receiver_account_id = response_body['receiver_account_id']
        self.money_amount = response_body['money_amount']
        self.point_amount = response_body['point_amount']
        self.description = response_body['description']
        self.bear_point_account_id = response_body['bear_point_account_id']
        self.point_expires_at = response_body['point_expires_at']
        self.status = response_body['status']
        self.error = response_body['error']
        self.lineno = response_body['lineno']
        self.transaction_id = response_body['transaction_id']
        self.created_at = response_body['created_at']
        self.updated_at = response_body['updated_at']

    def id(self):
        return self.id

    def bulk_transaction(self):
        return self.bulk_transaction

    def type(self):
        return self.type

    def sender_account_id(self):
        return self.sender_account_id

    def receiver_account_id(self):
        return self.receiver_account_id

    def money_amount(self):
        return self.money_amount

    def point_amount(self):
        return self.point_amount

    def description(self):
        return self.description

    def bear_point_account_id(self):
        return self.bear_point_account_id

    def point_expires_at(self):
        return self.point_expires_at

    def status(self):
        return self.status

    def error(self):
        return self.error

    def lineno(self):
        return self.lineno

    def transaction_id(self):
        return self.transaction_id

    def created_at(self):
        return self.created_at

    def updated_at(self):
        return self.updated_at

