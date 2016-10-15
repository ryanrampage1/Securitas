
class SymantecManagementServices:
    def __init__(self, client):
        self.client = client
        self.response = None

    def sendOtpSMS(self,client, requestId, userId, phoneNumber, isGatewayAcctInfo=False, onBehalfOfAccountId=None,
                   smsFrom=None, messageTemplate=None, gatewayId=None, gatewayPassword=None ):
        if isGatewayAcctInfo:
            res = self.client.service.sendOtp(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,userId=userId,
                                        smsDeliveryInfo={"phoneNumber": phoneNumber, "smsFrom": smsFrom,
                                        "messageTemplate":messageTemplate,
                                                         "gatewayAcctInfo":{"Id":gatewayId, "Password":gatewayPassword}})
        else:
            res = self.client.service.sendOtp(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, userId=userId,
                                        smsDeliveryInfo={"phoneNumber": phoneNumber, "smsFrom": smsFrom,
                                                         "messageTemplate": messageTemplate})
        self.response = str(res)
        print(self.response)
        pass
