import logging

#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)

class getCredentialInfo:

    def __init__(self,client, requestId, onBehalfOfAccountId,credentialId=-1, credentialType="STANDARD_OTP", includePushAttributes=True):
        self.client = client
        self.requestId = requestId
        self.onBehalfOfAccountId = onBehalfOfAccountId
        self.credentialId = credentialId
        self.credentialType = credentialType
        self.includePushAttributes = includePushAttributes


    def __str__(self):
        res = str(self.client.service.getCredentialInfo(requestId=self.requestId, onBehalfOfAccountId=self.onBehalfOfAccountId,credentialId=self.credentialId,
                                   credentialType=self.credentialType, includePushAttributes=self.includePushAttributes))
        return res

    def getFieldContent(self,fieldname):
        info_list = self.__str__().split('\n')

        for item in info_list:
            if fieldname in item:

                return item.split('=')[1][1:]
