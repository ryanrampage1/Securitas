import logging

def __init__(self,client, requestId):
    self.client = client
    self.requestId = requestId


def __str__(self):
    res = str(self.client.service.getUserInfo(requestId=self.requestId))
    return res


def getFieldContent(self, fieldname):
    info_list = self.__str__().split('\n')

    for item in info_list:
        if fieldname in item:
            return item.split('=')[1][1:]