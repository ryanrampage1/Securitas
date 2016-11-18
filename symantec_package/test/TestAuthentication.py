import unittest
from suds.client import Client
import symantec_package
from symantec_package.lib.userService.SymantecUserServices import SymantecUserServices
from symantec_package.HTTPHandler import setConnection, HTTPSClientAuthHandler, HTTPSClientCertTransport
from unittest.mock import Mock, patch

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        # the URLs for now which will have the WSDL files and the XSD file
        query_services_url = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
        userservices_url = 'http://webdev.cse.msu.edu/~morcoteg/Symantec/WSDL/vipuserservices-auth-1.7.wsdl'

        # initializing the Suds clients for each url, with the client certificate youll have in the same dir as this file
        query_services_client = Client(query_services_url,
                                       transport=HTTPSClientCertTransport('vip_certificate.crt', 'vip_certificate.crt'))
        user_services_client = Client(userservices_url,
                                      transport=HTTPSClientCertTransport('vip_certificate.crt', 'vip_certificate.crt'))

        self.test_user_services_object = SymantecUserServices(user_services_client)

    @patch('symantec_package.lib.userService.SymantecUserServices')
    def test_authenticateUser(self, mock):  # this goes for all the derivatives of this api call

        # authenticate_result = self.test_user_services_object.authenticateUser("test_otp", \
        #                                                             "gabe_phone", "991483")
        # self.assertTrue("0000" in str(authenticate_result))

        reply = {"requestId": "a123", "status": "0000", "statusMessage": "Success",
                 "authContext": {"params": {"Key": "authLevel.level", "Value": 10}}}

        mock.SymantecUserServices.authenticateUser.return_value = Mock()
        mock.authenticateUser.return_value.json.return_value = reply

        response = symantec_package.lib.userService.SymantecUserServices.authenticateNothing("testy", "Allen")
        self.assertTrue(response.json() != reply)

        response = symantec_package.lib.userService.SymantecUserServices.authenticateUser("testy", "Allen")

        self.assertTrue((response.json()) == reply)

        self.assertTrue(response.json()["status"] == "0000")
        self.assertTrue(response.json()['requestId'] == "a123")
        self.assertTrue(response.json()['statusMessage'] == "Success")
        self.assertTrue(response.json()['authContext']['params']['Key'] == "authLevel.level")
        self.assertTrue(response.json()['authContext']['params']['Value'] == 10)

        pass

    @patch('symantec_package.lib.userService.SymantecUserServices')
    def test_authenticateCredentials(self, mock):  # this goes for all the derivatives of this api call (except push which is handled in next test)
        # authenticate_result = self.test_user_services_object.authenticateCredentialWithStandard_OTP("test_cred_otp", "VSMT16833399",
        #                                                                                             "374125")
        #
        # self.assertTrue("0000" in str(authenticate_result))

        reply = {"requestId": "ac123", "status": "0000", "statusMessage": "Success", "credentialId": "18001337",
                 "credentialType": "SMS_OTP", "transactionId": "RealTransactionId",
                 "authContext": {"params": {"Key": "authLevel.level", "Value": 10}}}

        mock.SymantecUserServices.authenticateCredentials.return_value = Mock()
        mock.authenticateCredentials.return_value.json.return_value = reply

        response = symantec_package.lib.userService.SymantecUserServices.authenticateNothing("testy", "Allen")
        self.assertTrue(response.json() != reply)

        response = symantec_package.lib.userService.SymantecUserServices.authenticateCredentials("testy", "Allen")

        self.assertTrue((response.json()) == reply)

        self.assertTrue(response.json()["status"] == "0000")
        self.assertTrue(response.json()['requestId'] == "ac123")
        self.assertTrue(response.json()['statusMessage'] == "Success")
        self.assertTrue(response.json()['credentialId'] == "18001337")
        self.assertTrue(response.json()['credentialType'] == "SMS_OTP")
        self.assertTrue(response.json()['transactionId'] == "RealTransactionId")
        self.assertTrue(response.json()['authContext']['params']['Key'] == "authLevel.level")
        self.assertTrue(response.json()['authContext']['params']['Value'] == 10)

        pass

    @patch('symantec_package.lib.userService.SymantecUserServices')
    def test_pushCredential(self, mock):
        reply = {"requestId": "ac123", "status": "6040", "statusMessage": "Mobile push request sent",
                 "pushDetail": {"pushCredentialId": "133709001", "pushSent": True}, "transactionId": "RealTransactionId",
                 "authContext": {"params": {"Key": "authLevel.level", "Value": 10}}}

        mock.SymantecUserServices.authenticateCredentials.return_value = Mock()
        mock.authenticateCredentials.return_value.json.return_value = reply

        response = symantec_package.lib.userService.SymantecUserServices.authenticateNothing()
        self.assertTrue(response.json() != reply)

        response = symantec_package.lib.userService.SymantecUserServices.authenticateCredentials("Parameters Here!")

        self.assertTrue((response.json()) == reply)

        self.assertTrue(response.json()["status"] == "6040")
        self.assertTrue(response.json()['requestId'] == "ac123")
        self.assertTrue(response.json()['statusMessage'] == "Mobile push request sent")
        self.assertTrue(response.json()["pushDetail"]['pushCredentialId'] == "133709001")
        self.assertTrue(response.json()["pushDetail"]['pushSent'] == True)
        self.assertTrue(response.json()['transactionId'] == "RealTransactionId")
        self.assertTrue(response.json()['authContext']['params']['Key'] == "authLevel.level")
        self.assertTrue(response.json()['authContext']['params']['Value'] == 10)


        pass

    @patch('symantec_package.lib.userService.SymantecUserServices')
    def test_pushUser(self, mock):
        # authenticate_result = self.test_user_services_object.authenticateCredentialWithPush("push_456", "VSMT16833399",
        #                                                                                "Use my Push!")
        # print(str(authenticate_result))
        # self.assertTrue("6040" in str(authenticate_result))
        reply = {"requestId": "ac123", "status": "6040", "statusMessage": "Mobile push request sent",
                 "pushDetail": {"pushCredentialId": "133709001", "pushSent": True},
                 "transactionId": "RealTransactionId",
                 "authContext": {"params": {"Key": "authLevel.level", "Value": 10}}}

        mock.SymantecUserServices.authenticateUserWithPush.return_value = Mock()
        mock.authenticateUserWithPush.return_value.json.return_value = reply

        response = symantec_package.lib.userService.SymantecUserServices.authenticateUserWithNothing()
        self.assertTrue(response.json() != reply)

        response = symantec_package.lib.userService.SymantecUserServices.authenticateUserWithPush("Parameters Here!")

        self.assertTrue((response.json()) == reply)

        self.assertTrue(response.json()["status"] == "6040")
        self.assertTrue(response.json()['requestId'] == "ac123")
        self.assertTrue(response.json()['statusMessage'] == "Mobile push request sent")
        self.assertTrue(response.json()["pushDetail"]['pushCredentialId'] == "133709001")
        self.assertTrue(response.json()["pushDetail"]['pushSent'] is True)
        self.assertTrue(response.json()['transactionId'] == "RealTransactionId")
        self.assertTrue(response.json()['authContext']['params']['Key'] == "authLevel.level")
        self.assertTrue(response.json()['authContext']['params']['Value'] == 10)

        pass

    @patch('symantec_package.lib.userService.SymantecUserServices')
    def test_checkOtp(self, mock):
        reply = {"requestId": "123", "status": "0000", "statusMessage": "Success", "credentialId": "VSTZ1337",
                 "credentialType": "STANDARD_OTP", "authContext": {"params": {"Key": "authLevel.level", "Value": 1}}}

        mock.SymantecUserServices.checkOtp.return_value = Mock()
        mock.checkOtp.return_value.json.return_value = reply

        response = symantec_package.lib.userService.SymantecUserServices.checkOut("checkOutyou")
        self.assertTrue(response.json() != reply)

        response = symantec_package.lib.userService.SymantecUserServices.checkOtp("PARAMS")

        self.assertTrue((response.json()) == reply)

        self.assertTrue(response.json()["status"] == "0000")
        self.assertTrue(response.json()['requestId'] == "123")
        self.assertTrue(response.json()['statusMessage'] == "Success")
        self.assertTrue(response.json()['credentialId'] == "VSTZ1337")
        self.assertTrue(response.json()['credentialType'] == "STANDARD_OTP")
        self.assertTrue(response.json()['authContext']['params']['Key'] == "authLevel.level")
        self.assertTrue(response.json()['authContext']['params']['Value'] == 1)

        pass

    @patch('symantec_package.lib.userService.SymantecUserServices')
    def test_confirmRisk(self, mock):
        reply = {"requestId": "12345", "status": "0000", "statusMessage": "Success",
                 "KeyValuePairs": {"Key": "device.feedback", "Value": True}}

        mock.SymantecUserServices.confirmRisk.return_value = Mock()
        mock.confirmRisk.return_value.json.return_value = reply

        response = symantec_package.lib.userService.SymantecUserServices.checkOutRisk("checkOutyou")
        self.assertTrue(response.json() != reply)

        response = symantec_package.lib.userService.SymantecUserServices.confirmRisk("PARAMS")

        self.assertTrue((response.json()) == reply)

        self.assertTrue(response.json()["status"] == "0000")
        self.assertTrue(response.json()['requestId'] == "12345")
        self.assertTrue(response.json()['statusMessage'] == "Success")
        self.assertTrue(response.json()['KeyValuePairs']['Key'] == "device.feedback")
        self.assertTrue(response.json()['KeyValuePairs']['Value'] is True)


        pass

    @patch('symantec_package.lib.userService.SymantecUserServices')
    def test_evaluateRisk(self, mock):
        reply = {"requestId": "12345", "status": "0000", "statusMessage": "Success", "Risky": False, "RiskScore": 0,
                 "RiskThreshold": 9001, "RiskReason": "Device reputation", "PolicyVersion": 1.0, "eventId": 1337,
                 "KeyValuePairs": [{"KeyValuePair": {"Key": "device.expired", "Value": False}},
                                   {"KeyValuePair": {"Key": "device.registered", "Value": True}},
                                   {"KeyValuePair": {"Key": "device.shared", "Value": False}},
                                   {"KeyValuePair": {"Key": "device.tag.id", "Value": "abc123"}},
                                   {"KeyValuePair": {"Key": "device.friendly.name", "Value": "CoolDevice"}}]}

        mock.SymantecUserServices.denyRisk.return_value = Mock()
        mock.denyRisk.return_value.json.return_value = reply

        response = symantec_package.lib.userService.SymantecUserServices.checkOutRisk("checkOutyou")
        self.assertTrue(response.json() != reply)

        response = symantec_package.lib.userService.SymantecUserServices.denyRisk("PARAMS")

        self.assertTrue((response.json()) == reply)

        self.assertTrue(response.json()["status"] == "0000")
        self.assertTrue(response.json()['requestId'] == "12345")
        self.assertTrue(response.json()['statusMessage'] == "Success")
        self.assertTrue(response.json()['Risky'] is False)
        self.assertTrue(response.json()['RiskScore'] == 0)
        self.assertTrue(response.json()['RiskThreshold'] == 9001)
        self.assertTrue(response.json()['RiskReason'] == "Device reputation")
        self.assertTrue(response.json()['PolicyVersion'] == 1.0)
        self.assertTrue(response.json()['eventId'] == 1337)
        self.assertTrue(response.json()['KeyValuePairs'][0]["KeyValuePair"]['Key'] == "device.expired")
        self.assertTrue(response.json()['KeyValuePairs'][0]["KeyValuePair"]['Value'] is False)
        self.assertTrue(response.json()['KeyValuePairs'][1]["KeyValuePair"]['Key'] == "device.registered")
        self.assertTrue(response.json()['KeyValuePairs'][1]["KeyValuePair"]['Value'] is True)
        self.assertTrue(response.json()['KeyValuePairs'][2]["KeyValuePair"]['Key'] == "device.shared")
        self.assertTrue(response.json()['KeyValuePairs'][2]["KeyValuePair"]['Value'] is False)
        self.assertTrue(response.json()['KeyValuePairs'][3]["KeyValuePair"]['Key'] == "device.tag.id")
        self.assertTrue(response.json()['KeyValuePairs'][3]["KeyValuePair"]['Value'] == "abc123")
        self.assertTrue(response.json()['KeyValuePairs'][4]["KeyValuePair"]['Key'] == "device.friendly.name")
        self.assertTrue(response.json()['KeyValuePairs'][4]["KeyValuePair"]['Value'] == "CoolDevice")

        pass

    @patch('symantec_package.lib.userService.SymantecUserServices')
    def test_denyRisk(self, mock):
        reply = {"requestId": "12345", "status": "0000", "statusMessage": "Success",
                 "KeyValuePairs": [{"KeyValuePair": {"Key": "device.feedback", "Value": True}},
                                   {"KeyValuePair": {"Key": "device.tag.id", "Value": "abc123"}},
                                   {"KeyValuePair": {"Key": "device.friendly.name", "Value": "CoolDevice"}}]}

        mock.SymantecUserServices.denyRisk.return_value = Mock()
        mock.denyRisk.return_value.json.return_value = reply

        response = symantec_package.lib.userService.SymantecUserServices.checkOutRisk("checkOutyou")
        self.assertTrue(response.json() != reply)

        response = symantec_package.lib.userService.SymantecUserServices.denyRisk("PARAMS")

        self.assertTrue((response.json()) == reply)

        self.assertTrue(response.json()["status"] == "0000")
        self.assertTrue(response.json()['requestId'] == "12345")
        self.assertTrue(response.json()['statusMessage'] == "Success")
        self.assertTrue(response.json()['KeyValuePairs'][0]["KeyValuePair"]['Key'] == "device.feedback")
        self.assertTrue(response.json()['KeyValuePairs'][0]["KeyValuePair"]['Value'] is True)
        self.assertTrue(response.json()['KeyValuePairs'][1]["KeyValuePair"]['Key'] == "device.tag.id")
        self.assertTrue(response.json()['KeyValuePairs'][1]["KeyValuePair"]['Value'] == "abc123")
        self.assertTrue(response.json()['KeyValuePairs'][2]["KeyValuePair"]['Key'] == "device.friendly.name")
        self.assertTrue(response.json()['KeyValuePairs'][2]["KeyValuePair"]['Value'] == "CoolDevice")

        pass

if __name__ == '__main__':
    unittest.main()