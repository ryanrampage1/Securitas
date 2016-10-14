
class authenticateCredentials:
    def __init__(self, client, requestId, activate, credentials, otpAuthData=None, pushAuthData=None):
        self.client = client
        self.requestId = requestId
        self.credentials = credentials
        self.otpAuthData = otpAuthData
        self.pushAuthData = pushAuthData
        self.activate = activate

    def __str__(self):
        res = str(self.client.service.authenticateCredentials(requestId=self.requestId, credentials=self.credentials,
                                   otpAuthData=self.otpAuthData, pushAuthData=self.pushAuthData, activate=self.activate))
        return res