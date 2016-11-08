"""
.. module:: SymantecUserServices
    :platform: All platforms that are compatible with Python framework
    :synopsis: Module handles all VIP user services SOAP calls

.. moduleauthor:: Gabriel Morcote & Allen Huynh

"""

import string
import random       #random/string to generate random request IDs

### A class to represent the functions that Symantec User Services provides
class SymantecUserServices:
    """This class acts as a layer of abstraction to handling all user services Symantec VIP SOAP calls in Python.

        You call this class to handle anything that is related to authenticating users and credentials.

        Example:
            >>> client = Client("http://../vipuserservices-auth-1.7.wsdl", transport = HTTPSClientCertTransport('vip_certificate.crt','vip_certificate.crt'))
            >>> service = SymantecUserServices(client)
            >>> response = service.authenticateUser(<parameters here>)
            >>> print (response)

        .. NOTE::
            Reference HTTPHandler for further information on how to setup the client.

        """

    def __init__(self, client):
        """The class takes in only a SOAP client object.

            Arg:
                client (suds.client Client): The client to handle the SOAP calls

            .. NOTE::
                Any parameters that are of "None" type are optional fields.

        """
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
    #     self.response = res
    #     # print(res)
    #     return res


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
        self.response = res
        # print(res)
        return res


    #Fix this to cover all parameters in SOAP call
    def authenticateCredentials(self, requestId, credentials, otp1=None, pushAuthData=None, activate=None, authContext=None, onBehalfOfAccountId=None):
        res = self.client.service.authenticateCredentials(requestId=requestId, credentials=credentials, onBehalfOfAccountId=onBehalfOfAccountId,
                                                          otpAuthData={"otp": otp1}, pushAuthData=pushAuthData, activate=activate, authContext=authContext
                                                          )
        self.response = res
        # print(self.response)
        return res



    ## KLJSDHFLKSJDHFLSKDJFHLSKDJFHSLKDJFHSLKDJFHSDLKFJHSDLKFJDHFS ***************!!!!!

    def authenticateCredentialWithPush(self, requestId, credentialId, pushMessage,
                                       displayTitle=None, displayMessage=None, displayProfile=None, activate=None,
                                                authContext=None, value=None, timeout=None):
        """
                    :description: *Authenticates a user via a Push notification using their credential ID.*
                    :note:
                    :param requestId: A unique identifier of the request for the enterprise application. This may be useful for troubleshooting
                    :type requestId: string
                    :param userId: Unique user ID (i.e.- email address, login name). Accepts 1 - 128 characters. Case-sensitive.
                    :type userId: string
                    :param pushMessage: Text of the push notification in Notification Center (iOS) or Notification Drawer (Android). Suggested maximum size 70 characters.
                    :type pushMessage: string
                    :param displayTitle: Title of the modal. Suggested maximum size 30 characters.
                    :type displayTitle: string
                    :param displayMessage: Text of modal. Suggested maximum size 70 characters.
                    :type displayMessage: string
                    :param displayProfile: Indicates the login URL or profile. Suggested maximum size 60 characters.
                    :type displayProfile: string
                    :param activate: Activates a credential. If otpAuthData is provided, it consumes the OTP to authenticate. If pushAuthData is used, sends a push notification to the credential for authentication.
                    :type activate: boolean
                    :param authContext: A map containing the parameters that control how the authentication is performed. VIP User Services accepts an authentication level for the authContext field. The authentication level defines the credential types that can be validated with this request. This level must match an authentication level configured in VIP Manager. ■ Key: Enter authLevel.level ■ Value: Enter the authentication level value (as an integer from 1 - 10).
                    :type authContext: string
                    :param value: The user's specified gateway Account password
                    :type value: string
                    :param timeout: The user's specified gateway Account password
                    :type timeout: string
                    :returns: string -- the return SOAP response.
                    :raises:

                """
        if pushMessage is not None:
            res = self.client.service.authenticateCredentials(requestId=requestId,
                                                              credentials={"credentialId": credentialId,
                                                                           "credentialType": "STANDARD_OTP"},
                                                              activate=activate, otpAuthData=None,
                                                              pushAuthData={"displayParameters":
                                                                                {"Key": "push.message.text",
                                                                                 "Value": pushMessage}
                                                                            # {"Key":"display.message.text", "Value":displayMessage}
                                                                            })


        if displayTitle is not None:

            if displayProfile is not None:
                pass

            pass

        return res



    #Fix this as well!
    def authenticateCredentialWithSMS(self, requestId, credentialId_phoneNumber, securityCode, activate=None):
        if activate is not None:
            res = self.client.service.authenticateCredentials(requestId=requestId, activate=activate,
                                                          credentials={"credentialId": credentialId_phoneNumber,
                                                                       "credentialType": "SMS_OTP"},
                                                          otpAuthData={"otp": securityCode})
            self.response = res
            # print(self.response)
            return res
        res = self.client.service.authenticateCredentials(requestId=requestId,
                                                          credentials={"credentialId": credentialId_phoneNumber,
                                                                       "credentialType": "SMS_OTP"},
                                                          otpAuthData={"otp": securityCode})
        self.response = res
        # print(self.response)
        return res

    #Fix this as well!
    def authenticateCredentialWithStandard_OTP(self, requestId, credentialId, securityCode, activate=None):
        if activate is not None:
            res = self.client.service.authenticateCredentials(requestId=requestId, activate=activate,
                                                              credentials={"credentialId": credentialId,
                                                                           "credentialType": "STANDARD_OTP"},
                                                              otpAuthData={"otp": securityCode})
            self.response = res
            return res

        res = self.client.service.authenticateCredentials(requestId=requestId,
                                                          credentials={"credentialId": credentialId,
                                                                       "credentialType": "STANDARD_OTP"},
                                                          otpAuthData={"otp": securityCode})
        self.response = res
        # print(self.response)
        return res


    # FIX...Missing a ton of parameters and structured wrong with authContext --> key and value!
    def authenticateUserWithPush(self, requestId, userId, pin=None, displayParams=None, requestParams=None, authContext=None):
        res = self.client.service.authenticateUserWithPush(requestId=requestId, userId=userId)
        self.response = res
        # print(self.response)
        return res


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
        self.response = res
        # print(res)
        return res

    def confirmRisk(self, requestId, UserId, EventId, VerifyMethod=None, KeyValuePair=None, onBehalfOfAccountId=None):
        # note: keyValuePair is a list containing key + value
        res = self.client.service.confirmRisk(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, UserId=UserId,
                                              EventId=EventId, VerifyMethod=VerifyMethod, KeyValuePair=KeyValuePair)
        self.response = res
        # print(res)
        return res

    def denyRisk(self, requestId, UserId, EventId, VerifyMethod=None, IAAuthData=None, isRememberDevice=None,
                 FriendlyName=None, KeyValuePair=None, onBehalfOfAccountId=None):
        res = self.client.service.denyRisk(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                              UserId=UserId, EventId=EventId, VerifyMethod=VerifyMethod, IAAuthData=IAAuthData,
                                              RememberDevice=isRememberDevice, FriendlyName=FriendlyName, KeyValuePair=KeyValuePair)
        self.response = res
        # print(res)
        return res

    def evaluateRisk(self, requestId, UserId, IpAddress, UserAgent, IAAuthData=None, KeyValuePair=None, onBehalfOfAccountId=None):
        res = self.client.service.evaluateRisk(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, UserId=UserId,
                                               Ip=IpAddress, UserAgent=UserAgent, IAAuthData=IAAuthData, KeyValuePair=KeyValuePair)
        self.response = res
        # print (res)
        return res

    def getFieldContent(self, fieldname):
        info_list = self.response.split('\n')
        for item in info_list:
            if fieldname in item:
                return item.split('=')[1][1:]
