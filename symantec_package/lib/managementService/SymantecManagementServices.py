"""
.. module:: Symantec Management Service
    :platform: All platforms that are compatible with Python framework
    :synopsis: Module handles all VIP management SOAP calls

.. moduleauthor:: Allen Huynh
"""

class SymantecManagementServices:
    """This class acts as a layer of abstraction to handling all Symantec VIP SOAP calls in Python.

    You call this class to handle anything that is related to managing users and credentials.

    Example:
        >>> client = Client("http://../vipuserservices-mgmt-1.7.wsdl", transport = HTTPSClientCertTransport('vip_certificate.crt','vip_certificate.crt'))
        >>> service = SymantecManagementServices(client)
        >>> response = service.sendOtpSMS(<parameters here>)
        >>> print (response)

    .. NOTE::
        Reference HTTPHandler for further information on how to setup the client.

    """

    def __init__(self, client):
        """TThe class takes in only a SOAP client object.

            Arg:
                client (suds.client Client): The client to handle the SOAP calls

        """
        self.client = client
        self.response = None

    def sendOtpSMS(self, requestId, userId, phoneNumber, isGatewayAcctInfo=False, onBehalfOfAccountId=None,
                   smsFrom=None, messageTemplate=None, gatewayId=None, gatewayPassword=None ):
        """
            :description: *Sends a one time password to a mobile phone.*
            :param requestId: A unique identifier of the request for the enterprise application. This may be useful for troubleshooting
            :type requestId: string
            :param userId: Unique user ID (i.e.- email address, login name). Accepts 1 - 128 characters. Case-sensitive.
            :type userId: string
            :param phoneNumber: The mobile number credential tied to user (active).
            :type phoneNumber: string
            :param isGatewayAcctInfo: Should we use a gateway?
            :type isGatewayAcctInfo: bool
            :param onBehalfOfAccountId: The Id that this request is done on behalf of.
            :type onBehalfOfAccountId: string
            :param smsFrom: DEPRECATED - Specifies the FROM number that is used to send an SMS message so that the message from receiver can be mapped back.
            :type smsFrom: string
            :param messageTemplate: The text that is sent to the user's SMS device along with security code.
            :type messageTemplate: string ???
            :param gatewayId: The user's specified gateway Account Id
            :type gatewayId: string
            :param gatewayPassword: The user's specified gateway Account password
            :type gatewayPassword: string
            :returns: string -- the return SOAP response.
            :raises:

        """

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
        # print(self.response)
        return str(res)

    # simple create user function. check for tests LOOK AND WRITE SOME TOO if you think needed
    def createUser(self, requestId, userId, onBehalfOfAccountId=None, pin=None, forcePinChange=None):
        res = self.client.service.createUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, \
                                             userId=userId, pin=pin, forcePinChange=forcePinChange)
        # print(str(res))
        self.response = str(res)
        return str(res)

    #simple delete user function
    def deleteUser(self, requestId, userId, onBehalfOfAccountId=None):
        res = self.client.service.deleteUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, \
                                             userId=userId)
        # print(str(res))
        self.response = str(res)
        return str(res)


    def updateUser(self, requestId, userId, newUserId=None, newUserStatus=None, oldPin=None,
                   newPin=None, forcePinChange=None, onBehalfOfAccountId=None):
        res = self.client.service.updateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                             userId=userId, newUserId=newUserId, newUserStatus=newUserStatus, oldPin=oldPin,
                                             newPin=newPin, forcePinChange=forcePinChange)
        # print(str(res))
        self.response = str(res)
        return str(res)

    def registerBySMS(self, requestId, phoneNumber,smsFrom=None, messageTemplate=None, gatewayId=None, gatewayPassword=None
                      ,onBehalfOfAccountId=None):
        if gatewayId == None or gatewayPassword == None:
            res = self.client.service.register(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                               smsDeliveryInfo ={"phoneNumber": phoneNumber, "smsFrom": smsFrom,
                                                 "messageTemplate": messageTemplate},
                                               voiceDeliveryInfo=None, serviceOtpDeliveryInfo=None)
        else:
            res = self.client.service.register(requestId=requestId,onBehalfOfAccountId=onBehalfOfAccountId, smsDeliveryInfo
                                               ={"phoneNumber":phoneNumber, "smsFrom":smsFrom, "messageTemplate":messageTemplate,
                                                 "gatewayAcctInfo": {"Id": gatewayId,"Password":gatewayPassword}},
                                               voiceDeliveryInfo=None, serviceOtpDeliveryInfo=None)
        # print(str(res))
        self.response = str(res)
        return str(res)

    def registerByVoice(self, requestId, phoneNumber, language=None, onBehalfOfAccountId=None):
        res = self.client.service.register(requestId=requestId,onBehalfOfAccountId=onBehalfOfAccountId, smsDeliveryInfo=None,
                                           voiceDeliveryInfo={"phoneNumber":phoneNumber, "Language":language},
                                           serviceOtpDeliveryInfo=None)
        # print(str(res))
        self.response = str(res)
        return str(res)

    def registerByServiceOtp(self, requestId, serviceOtpId, onBehalfOfAccountId=None):
        res = self.client.service.register(requestId=requestId,onBehalfOfAccountId=onBehalfOfAccountId, smsDeliveryInfo=None,
                                           voiceDeliveryInfo=None,serviceOtpDeliveryInfo={"id":serviceOtpId})
        # print(str(res))
        self.response = str(res)
        return str(res)

    #Add credential to existing user
    # def addCredentialOtp(self, requestId, userId, credentialId, credentialType, otp1, otp2=None,friendlyName=None,
    #                          trustedCredentialDevice=None, trustedDevice=None,onBehalfOfAccountId=None):
    #     if trustedDevice == None:
    #         res = self.client.service.addCredential(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, userId=userId,
    #                                                 credentialDetail= {"credentialId":credentialId, "credentialType": credentialType,
    #                                                                    "friendlyName":friendlyName, "trustedDevice":trustedCredentialDevice},
    #                                                 otpAuthData={"otp":otp1,"otp2":otp2}, trustedDevice=None)
    #     else:
    #         res = self.client.service.addCredential(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, userId=userId,
    #                                                 credentialDetail= {"credentialId":credentialId, "credentialType": credentialType,
    #                                                                    "friendlyName":friendlyName, "trustedDevice":trustedCredentialDevice},
    #                                                 otpAuthData=None, trustedDevice=trustedDevice)
    #     print(str(res))
    #     self.response = str(res)
    #     return str(res)

    def addCredentialOtp(self, requestId, userId, credentialId, credentialType, otp1, otp2=None, friendlyName=None,
                         trustedCredentialDevice=None, onBehalfOfAccountId=None):
        res = self.client.service.addCredential(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                userId=userId,
                                                credentialDetail= {"credentialId":credentialId, "credentialType": credentialType,
                                                        "friendlyName":friendlyName, "trustedDevice":trustedCredentialDevice},
                                                otpAuthData={"otp":otp1,"otp2":otp2}, trustedDevice=None)
        # print(str(res))
        self.response = str(res)
        return str(res)

    def addCredentialTrustedDevice(self, requestId, userId, credentialId, credentialType, trustedDevice,
                                   friendlyName=None, trustedCredentialDevice=None, onBehalfOfAccountId=None):
        res = self.client.service.addCredential(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                userId=userId,
                                                credentialDetail={"credentialId": credentialId,
                                                                  "credentialType": credentialType,
                                                                  "friendlyName": friendlyName,
                                                                  "trustedDevice": trustedCredentialDevice},
                                                otpAuthData=None, trustedDevice=trustedDevice)
        # print(str(res))
        self.response = str(res)
        return str(res)

    #Remove a user's credential
    def removeCredential(self, requestId, userId, credentialId, credentialType, trustedDevice=None, onBehalfOfAccountId=None):
        res = self.client.service.removeCredential(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,userId=userId,
                                                   credentialId=credentialId, credentialType=credentialType, trustedDevice=trustedDevice)
        self.response = str(res)
        # print(self.response)
        return self.response

    def updateCredential(self, requestId, userId, credentialId, credentialType, friendlyName, onBehalfOfAccountId=None):
        res = self.client.service.updateCredential(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,userId=userId,
                                                   credentialId=credentialId, credentialType=credentialType, friendlyName=friendlyName)
        self.response = str(res)
        # print(self.response)
        return self.response


    def setTemporaryPasswordSMSDelivery(self, requestId, userId, phoneNumber, smsFrom=None, messageTemplate=None,
                                        gatewayId=None, gatewayPassword=None, temporaryPassword=None, expirationDate=None,
                                        oneTimeUseOnly=None, onBehalfOfAccountId=None):
        if gatewayId == None or gatewayPassword == None:
            if expirationDate == None and oneTimeUseOnly == None:
                res = self.client.service.setTemporaryPassword(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                               userId=userId, temporaryPassword=temporaryPassword,
                                                               temporaryPasswordAttributes=None,
                                                               smsDeliveryInfo={"phoneNumber":phoneNumber, "smsFrom": smsFrom,
                                                                                "messageTemplate":messageTemplate,
                                                                                "gatewayAcctInfo":None})
            else:
                res = self.client.service.setTemporaryPassword(requestId=requestId,
                                                               onBehalfOfAccountId=onBehalfOfAccountId,
                                                               userId=userId, temporaryPassword=temporaryPassword,
                                                               temporaryPasswordAttributes={
                                                                   "expirationDate": expirationDate,
                                                                   "oneTimeUseOnly": oneTimeUseOnly},
                                                               smsDeliveryInfo={"phoneNumber": phoneNumber,
                                                                                "smsFrom": smsFrom,
                                                                                "messageTemplate": messageTemplate,
                                                                                "gatewayAcctInfo": None})
        else:
            if expirationDate == None and oneTimeUseOnly == None:
                res = self.client.service.setTemporaryPassword(requestId=requestId,
                                                               onBehalfOfAccountId=onBehalfOfAccountId,
                                                               userId=userId, temporaryPassword=temporaryPassword,
                                                               temporaryPasswordAttributes=None,
                                                               smsDeliveryInfo={"phoneNumber": phoneNumber,
                                                                                "smsFrom": smsFrom,
                                                                                "messageTemplate": messageTemplate,
                                                                                "gatewayAcctInfo": {"Id": gatewayId,
                                                                                                    "Password": gatewayPassword}})
            else:
                res = self.client.service.setTemporaryPassword(requestId=requestId,
                                                               onBehalfOfAccountId=onBehalfOfAccountId,
                                                               userId=userId, temporaryPassword=temporaryPassword,
                                                               temporaryPasswordAttributes={
                                                                   "expirationDate": expirationDate,
                                                                   "oneTimeUseOnly": oneTimeUseOnly},
                                                               smsDeliveryInfo={"phoneNumber": phoneNumber,
                                                                                "smsFrom": smsFrom,
                                                                                "messageTemplate": messageTemplate,
                                                                                "gatewayAcctInfo": {"Id": gatewayId,
                                                                                                    "Password": gatewayPassword}})
        self.response = str(res)
        # print(self.response)
        return self.response

    def setTemporaryPasswordVoiceDelivery(self, requestId, userId, phoneNumber, language=None, temporaryPassword=None,
                                          expirationDate=None, oneTimeUseOnly=None, onBehalfOfAccountId=None):
        if expirationDate == None and oneTimeUseOnly == None:
            res = self.client.service.setTemporaryPassword(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                           userId=userId, temporaryPassword=temporaryPassword,
                                                           temporaryPasswordAttributes=None, voiceDeliveryInfo={"phoneNumber":phoneNumber,
                                                                                                                "Language":language})
        else:
            res = self.client.service.setTemporaryPassword(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                           userId=userId, temporaryPassword=temporaryPassword,
                                                           temporaryPasswordAttributes={"expirationDate":expirationDate,
                                                                                        "oneTimeUseOnly":oneTimeUseOnly},
                                                           voiceDeliveryInfo={"phoneNumber": phoneNumber,
                                                                              "Language": language})
        self.response = str(res)
        # print(str(res))
        return self.response

    def setTemporaryPasswordAttributes(self, requestId, userId, expirationTime=None, oneTimeUseOnly=None, onBehalfOfAccountId=None):
        res = self.client.service.setTemporaryPasswordAttributes(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                                 userId=userId, expirationTime=expirationTime, oneTimeUseOnly=oneTimeUseOnly)
        self.response = str(res)
        # print(str(res))
        return self.response

    def clearTemporaryPassword(self, requestId, userId, onBehalfOfAccountId=None):
        res = self.client.service.clearTemporaryPin(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, userId=userId)
        self.response = str(res)
        # print(str(res))
        return self.response

    def clearUserPin(self, requestId, userId, onBehalfOfAccountId=None):
        res = self.client.service.clearUserPin(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, userId=userId)
        self.response = str(res)
        # print(str(res))
        return self.response

