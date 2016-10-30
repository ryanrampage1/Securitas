import string
import random       #random/string to generate random request IDs

### A class to represent the functions that Symantec User Services provides
class SymantecUserServices:

    def __init__(self, client):
        self.client = client
        self.response = None   #most recent response in str format
        # self.onBehalfOfAccountId = onBehalfOfAccountId
        # self.iaInfo = iaInfo
        # self.includePushAttributes = includePushAttributes


    ###  Call the client's authenticateUser function
    # def authenticateUser(self, requestId, userId, securityCode, pin=None, authContext=None, onBehalfOfAccountId=None):
    #     res = self.client.service.authenticateUser(requestId=requestId,onBehalfOfAccountId=onBehalfOfAccountId,
    #                                                userId=userId, otpAuthData={"otp": securityCode},
    #                                                pin=pin, authContext=authContext)
    #     self.response = str(res)
    #     # print(str(res))
    #     return str(res)


    # I fixed this one; Someone fix the following ones (low on time) - Allen
    def authenticateUser(self, requestId, userId, otp1, otp2=None, value=None, key="authLevel.level", pin=None, onBehalfOfAccountId=None):
        if otp2 == None:
            if value != None:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId, pin=pin, otpAuthData={"otp": otp1},
                                                       authContext={"params":{"Key":key, "Value":value}})
            else:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId, pin=pin, otpAuthData={"otp": otp1},
                                                       authContext=None)
        else:
            if value != None:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId, pin=pin, otpAuthData={"otp": otp1, "otp2": otp2},
                                                       authContext={"params": {"Key": key, "Value": value}})
            else:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId, pin=pin, otpAuthData={"otp": otp1, "otp2": otp2},
                                                       authContext=None)
        self.response = str(res)
        # print(str(res))
        return str(res)

    #Fix this to cover all parameters in SOAP call
    def authenticateCredentials(self, requestId, credentials, otpAuthData=None, pushAuthData=None, activate=None):
        res = self.client.service.authenticateCredentials(requestId=requestId, credentials=credentials, otpAuthData=otpAuthData)
        self.response = str(res)
        # print(self.response)
        return str(res)



    #Fix this as well!
    def authenticateWithSMS(self, requestId, credentialId_phoneNumber, securityCode, activate=None):
        res = self.client.service.authenticateCredentials(requestId=requestId, activate=activate,
                                                          credentials={"credentialId": credentialId_phoneNumber,
                                                                       "credentialType": "SMS_OTP"},
                                                          otpAuthData={"otp": securityCode})
        self.response = str(res)
         # print(self.response)
        return str(res)
    #Fix this as well!
    def authenticateWithStandard_OTP(self, requestId, credentialId, securityCode, activate=None):
        res = self.client.service.authenticateCredentials(requestId=requestId, activate= activate,
                                                          credentials={"credentialId": credentialId,
                                                                       "credentialType": "STANDARD_OTP"},
                                                          otpAuthData={"otp": securityCode})
        self.response = str(res)
        # print(self.response)
        return str(res)


    # FIX...Missing a ton of parameters and structured wrong with authContext --> key and value!
    def authenticateUserWithPush(self, requestId, userId, pin=None, displayParams=None, requestParams=None, authContext=None):
        res = self.client.service.authenticateUserWithPush(requestId=requestId, userId=userId)
        self.response = str(res)
        # print(self.response)
        return str(res)


    def checkOtp(self, requestId, userId, otp1, otp2=None, value=None, key="authLevel.level", onBehalfOfAccountId=None):
        if otp2 == None:
            if value != None:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId, otpAuthData={"otp": otp1},
                                                       authContext={"params":{"Key":key, "Value":value}})
            else:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId, otpAuthData={"otp": otp1},
                                                       authContext=None)
        else:
            if value != None:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId,  otpAuthData={"otp": otp1, "otp2": otp2},
                                                       authContext={"params": {"Key": key, "Value": value}})
            else:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId, otpAuthData={"otp": otp1, "otp2": otp2},
                                                       authContext=None)
        self.response = str(res)
        # print(str(res))
        return str(res)

    def confirmRisk(self, requestId, UserId, EventId, VerifyMethod=None, KeyValuePair=None, onBehalfOfAccountId=None):
        # note: keyValuePair is a list containing key + value
        res = self.client.service.confirmRisk(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, UserId=UserId,
                                              EventId=EventId, VerifyMethod=VerifyMethod, KeyValuePair=KeyValuePair)
        self.response = str(res)
        # print(str(res))
        return str(res)

    def denyRisk(self, requestId, UserId, EventId, VerifyMethod=None, IAAuthData=None, isRememberDevice=None,
                 FriendlyName=None, KeyValuePair=None, onBehalfOfAccountId=None):
        res = self.client.service.confirmRisk(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                              UserId=UserId, EventId=EventId, VerifyMethod=VerifyMethod, IAAuthData=IAAuthData,
                                              RememberDevice=isRememberDevice, FriendlyName=FriendlyName, KeyValuePair=KeyValuePair)
        self.response = str(res)
        # print(str(res))
        return str(res)

    def evaluateRisk(self, requestId, UserId, IpAddress, UserAgent, IAAuthData=None, KeyValuePair=None, onBehalfOfAccountId=None):
        res = self.client.service.evaluateRisk(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, UserId=UserId,
                                               Ip=IpAddress, UserAgent=UserAgent, IAAuthData=IAAuthData, KeyValuePair=KeyValuePair)
        self.response = str(res)
        # print (str(res))
        return str(res)

    def getFieldContent(self, fieldname):
        info_list = self.response.split('\n')
        for item in info_list:
            if fieldname in item:
                return item.split('=')[1][1:]
