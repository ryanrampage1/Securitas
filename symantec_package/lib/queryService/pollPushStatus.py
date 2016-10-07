import logging


class pollPushStatus:
    def __init__(self,client, requestId, onBehalfOfAccountId,transactionId):
        self.client = client
        self.requestId = requestId
        self.onBehalfOfAccountId = onBehalfOfAccountId
        self.transactionId = transactionId


    def __str__(self):
        res = str(self.client.service.getServerTime(requestId=self.requestId,onBehalfOfAccountId=self.onBehalfOfAccountId,
                                                    transactionId=self.transactionId))
        return res


    def getFieldContent(self, fieldname):
        info_list = self.__str__().split('\n')

        for item in info_list:
            if fieldname in item:
                return item.split('=')[1][1:]