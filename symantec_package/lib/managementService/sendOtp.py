
class sendOtp:
    def __init__(self,client, requestId, userId, smsDeliveryInfo=None, voiceDeliveryInfo=None):
        self.client = client
        self.requestId = requestId
        self.userId = userId
        self.smsDeliveryInfo = smsDeliveryInfo #phone number goes in here as {}

    def __str__(self):
        res = str(self.client.service.getUserInfo(requestId=self.requestId, userId=self.userId,
                                   smsDeliveryInfo=self.smsDeliveryInfo))
        return res