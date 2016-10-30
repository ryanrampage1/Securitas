
class SymantecServices:

    import sys
    sys.path.append("/home/oem/PycharmProjects/Securitas_Dev/Securitas") # remove this when finish

    from symantec_package.lib.userService.SymantecUserServices import SymantecUserServices
    from symantec_package.lib.queryService.SymantecQueryServices import SymantecQueryServices
    from symantec_package.lib.managementService.SymantecManagementServices import SymantecManagementServices

    def __init__(self, queryClient, managementClient, userClient):

        queryService = self.SymantecQueryServices(queryClient)
        managementService = self.SymantecManagementServices(managementClient)
        userService = self.SymantecUserServices(userClient)
        self.queryService = queryService
        self.managementService = managementService
        self.userService = userService
        self.queryClient = queryClient
        self.managementClient = managementClient
        self.userClient = userClient
        self.response  = None


# ******************** MULTIPLE CLIENT FUNCTIONS
    def authenticateUserWithPushThenPolling(self, requestIdPush, requestIdPoll, userId, queryTimeout=60, queryInterval=5,
                                            displayParams=None, requestParams=None, authContext=None, onBehalfOfAccountId=None):
        import time

        res = ""
        transaction_id = ""

        push = self.userService.authenticateUserWithPush(requestIdPush, userId)
        print (push)
        if self.userService.getFieldContent('transactionId') != None:
            transaction_id = self.userService.getFieldContent('transactionId').strip('"')
        else:
            # failed push should return
            return self.userService.getFieldContent('status')
        isExit = False
        isError = False

        for sec in range(1,queryTimeout // queryInterval):
            if isExit:
                break
            time.sleep(queryInterval) # NEED NEW SOLUTION for querying on interval in python

            #if sec % queryInterval == 0:
            poll_status = str(self.queryClient.service.pollPushStatus(requestId=requestIdPoll,
                                                                           onBehalfOfAccountId=onBehalfOfAccountId,
                                                                           transactionId=transaction_id))
            res = poll_status
            #now check response for status
            lines = poll_status.split('\n')
            for line in lines:
                if isError:
                    errorMessage = line.split('=')[1][1:].strip('\n')
                    print("\n\tError: " + errorMessage)
                    isExit = True
                    break
                if "status " in line:
                    status = line.split('=')[1][1:].strip('\n')
                    #res = status
                    if "0000" in status: # ignore this first status for polling connection
                        continue
                    elif "7000" in status:
                        print("\nSUCCESS! Push Accepted!")
                        isExit = True
                        break
                    elif "7001" in status:
                        print("\nIN PROGRESS...")
                        break
                    elif "7002" in status:
                        print("\nPush Denied!")
                        isExit = True
                        break
                    else:
                        #print("\n\tError status!")  # should later have it print status message
                        isError = True
        return(str(res))

# ******************** QUERY
    def getUserInfo(self, requestId, userId, onBehalfOfAccountId=None, iaInfo=True, includePushAttributes=True):
        res = self.queryService.getUserInfo(requestId, userId, onBehalfOfAccountId , iaInfo , includePushAttributes )
        self.response = res
        #print(self.response)
        return str(res)

    def pollPushStatus(self, requestId, transactionId):
        res = self.queryService.pollPushStatus( requestId,  transactionId)
        self.response = res
        #print(self.response)
        return str(res)

    def getCredentialInfo(self, requestId, credentialId, credentialType="STANDARD_OTP",
                          includePushAttributes=None, onBehalfOfAccountId=None):
        res = self.queryService.getCredentialInfo(requestId, credentialId, credentialType,
                          includePushAttributes , onBehalfOfAccountId )
        self.response = res
        #print(self.response)
        return str(res)

    def getServerTime(self, requestId, onBehalfOfAccountId=None):
        res = self.queryService.getServerTime(requestId, onBehalfOfAccountId)
        self.response = res
        #print(self.response)
        return str(res)

    def getTemporaryPasswordAttributes(self, requestId, userId, onBehalfOfAccountId=None):
        res = self.queryService.getTemporaryPasswordAttributes(requestId, userId, onBehalfOfAccountId)
        self.response = res
        #print(self.response)
        return str(res)

# ******************** MANAGEMENT
    def sendOtpSMS(self, requestId, userId, phoneNumber, isGatewayAcctInfo=False, onBehalfOfAccountId=None,
                   smsFrom=None, messageTemplate=None, gatewayId=None, gatewayPassword=None ):
        res = self.managementService.sendOtp(requestId, userId, phoneNumber, isGatewayAcctInfo, onBehalfOfAccountId,
                   smsFrom , messageTemplate, gatewayId, gatewayPassword )

        self.response = res
        # print(self.response)
        return str(res)

    # simple create user function. check for tests LOOK AND WRITE SOME TOO if you think needed
    def createUser(self, requestId, userId, onBehalfOfAccountId=None, pin=None, forcePinChange=None):
        res = self.managementService.createUser(requestId, userId, onBehalfOfAccountId , pin , forcePinChange )
        self.response = res
        # print(self.response)
        return str(res)

    #simple delete user function
    def deleteUser(self, requestId, userId, onBehalfOfAccountId=None):
        res = self.managementService.deleteUser(requestId, userId, onBehalfOfAccountId )
        self.response = res
        # print(self.response)
        return str(res)

    def updateUser(self, requestId, userId, newUserId=None, newUserStatus=None, oldPin=None,
                   newPin=None, forcePinChange=None, onBehalfOfAccountId=None):
        res = self.managementService.updateUser(requestId, userId, newUserId, newUserStatus, oldPin, newPin, forcePinChange, onBehalfOfAccountId)
        self.response = res
        # print(self.response)
        return str(res)

    def registerBySMS(self, requestId, phoneNumber, smsFrom=None, messageTemplate=None, gatewayId=None,
                      gatewayPassword=None, onBehalfOfAccountId=None):
        res = self.managementService.registerBySMS(requestId,phoneNumber,smsFrom,messageTemplate,gatewayId,gatewayPassword, onBehalfOfAccountId)
        self.response = res
        return str(res)

    def registerByVoice(self, requestId, phoneNumber, language=None, onBehalfOfAccountId=None):
        res = self.managementService.registerByVoice(requestId, phoneNumber, language, onBehalfOfAccountId)
        self.response = res
        return str(res)

    def registerByServiceOtp(self, requestId, serviceOtpId, onBehalfOfAccountId=None):
        res = self.managementService.registerByServiceOtp(requestId, serviceOtpId, onBehalfOfAccountId)
        self.response = res
        return str(res)

    def addCredentialOtp(self, requestId, userId, credentialId, credentialType, otp1, otp2=None, friendlyName=None,
                         trustedCredentialDevice=None, onBehalfOfAccountId=None):
        res = self.managementService.addCredentialOtp(requestId,userId,credentialId,credentialType,otp1,otp2,friendlyName,
                                                      trustedCredentialDevice, onBehalfOfAccountId)
        self.response = res
        return str(res)

    def addCredentialTrustedDevice(self, requestId, userId, credentialId, credentialType, trustedDevice,
                                   friendlyName=None, trustedCredentialDevice=None, onBehalfOfAccountId=None):
        res = self.managementService.addCredentialTrustedDevice(requestId, userId, credentialId, credentialType, trustedDevice,
                                   friendlyName, trustedCredentialDevice, onBehalfOfAccountId)
        self.response = res
        return str(res)

    def removeCredential(self, requestId, userId, credentialId, credentialType, trustedDevice=None,onBehalfOfAccountId=None):
        res = self.managementService.removeCredential(requestId, userId, credentialId, credentialType, trustedDevice,onBehalfOfAccountId)
        self.response = res
        return str(res)

    def updateCredential(self, requestId, userId, credentialId, credentialType, friendlyName, onBehalfOfAccountId=None):
        res = self.managementService.updateCredential(requestId, userId, credentialId, credentialType, friendlyName, onBehalfOfAccountId)
        self.response =res
        return str(res)

    def setTemporaryPasswordSMSDelivery(self, requestId, userId, phoneNumber, smsFrom=None, messageTemplate=None,
                                        gatewayId=None, gatewayPassword=None, temporaryPassword=None,expirationDate=None,
                                        oneTimeUseOnly=None, onBehalfOfAccountId=None):
        res = self.managementService.setTemporaryPasswordSMSDelivery(requestId, userId, phoneNumber, smsFrom, messageTemplate,
                                        gatewayId, gatewayPassword, temporaryPassword,expirationDate,
                                        oneTimeUseOnly, onBehalfOfAccountId)
        self.response = res
        return str(res)

    def setTemporaryPasswordVoiceDelivery(self, requestId, userId, phoneNumber, language=None, temporaryPassword=None,
                                          expirationDate=None, oneTimeUseOnly=None, onBehalfOfAccountId=None):
        res = self.managementService.setTemporaryPasswordVoiceDelivery(requestId, userId, phoneNumber, language, temporaryPassword,
                                          expirationDate, oneTimeUseOnly, onBehalfOfAccountId)
        self.response = res
        return str(res)

    def setTemporaryPasswordAttributes(self, requestId, userId, expirationTime=None, oneTimeUseOnly=None,onBehalfOfAccountId=None):
        res = self.managementService.setTemporaryPasswordAttributes(requestId,userId,expirationTime,oneTimeUseOnly,onBehalfOfAccountId)
        self.response =res
        return str(res)

    def clearTemporaryPassword(self, requestId, userId, onBehalfOfAccountId=None):
        res = self.managementService.clearTemporaryPassword(requestId,userId,onBehalfOfAccountId)
        self.response = res
        return str(res)

    def clearUserPin(self, requestId, userId, onBehalfOfAccountId=None):
        res = self.managementService.clearUserPin(requestId,userId,onBehalfOfAccountId)
        self.response = res
        return str(res)


# ********************USER SERVICE
    def authenticateUser(self, requestId, userId, otp1, otp2=None, value=None, key="authLevel.level", pin=None, onBehalfOfAccountId=None):
        res = self.userService.authenticateUser(requestId,  userId, otp1, otp2, value, key, pin, onBehalfOfAccountId)
        self.response = res
        # print(self.response)
        return str(res)

    # FIX when user service is updated
    def authenticateCredentials(self, requestId, credentials, otpAuthData=None, pushAuthData=None, activate=None):
        res = self.userService.authenticateCredentials( requestId,  credentials, otpAuthData, pushAuthData, activate)
        self.response = res
        # print(self.response)
        return str(res)

    ## FIX when user service is updated
    def authenticateWithSMS(self, requestId, credentialId_phoneNumber, securityCode, activate=None):
        res = self.userService.authenticateCredentials(requestId, credentialId_phoneNumber, securityCode, activate )

        self.response = res
        # print(self.response)
        return str(res)
        # FIX when user service is updated
    def authenticateWithStandard_OTP(self, requestId, credentialId, securityCode, activate=None):
        res = self.userService.authenticateCredentials(requestId, credentialId, securityCode, activate)

        self.response = res
        # print(self.response)
        return str(res)

    # FIX when user service is updated
    def authenticateUserWithPush(self, requestId, userId, pin=None, displayParams=None, requestParams=None, authContext=None):
        res = self.userService.authenticateUserWithPush(requestId, userId, pin, displayParams , requestParams , authContext )

        self.response = res
        # print(self.response)
        return str(res)

    def confirmRisk(self, requestId, UserId, EventId, VerifyMethod=None, KeyValuePair=None, onBehalfOfAccountId=None):
        res = self.userService.confirmRisk(requestId, UserId, EventId, VerifyMethod, KeyValuePair, onBehalfOfAccountId)

        self.response = res
        # print(self.response)
        return str(res)

    def denyRisk(self, requestId, UserId, EventId, VerifyMethod=None, IAAuthData=None, isRememberDevice=None,
                 FriendlyName=None, KeyValuePair=None, onBehalfOfAccountId=None):
        res = self.userService.denyRisk(requestId, UserId, EventId, VerifyMethod, IAAuthData, isRememberDevice,
                                        FriendlyName, KeyValuePair, onBehalfOfAccountId)
        self.response = res
        # print(self.response)
        return str(res)

    def evaluateRisk(self, requestId, UserId, IpAddress, UserAgent, IAAuthData=None, KeyValuePair=None,
                     onBehalfOfAccountId=None):
        res = self.userService.evaluateRisk(requestId,UserId, IpAddress, UserAgent, IAAuthData, KeyValuePair, onBehalfOfAccountId)
        self.response = res

        return str(res)

    def checkOtp(self, requestId, userId, otp1, otp2=None, value=None, key="authLevel.level", onBehalfOfAccountId=None):
        res = self.userService.checkOtp(requestId, userId, otp1, otp2, value, key, onBehalfOfAccountId)
        self.response = res
        return str(res)

    def getFieldContent(self, fieldname):
        self.response = str(self.response)
        info_list = self.response.split('\n')
        for item in info_list:
            if fieldname in item:
                return item.split('=')[1][1:]
