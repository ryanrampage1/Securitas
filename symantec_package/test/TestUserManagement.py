import unittest
from unittest.mock import Mock, patch
from suds.client import Client
import sys
import symantec_package

sys.path.append("/home/gabriel/Projects/PythonProjects/Symantec/Securitas/symantec_package/lib/managementService")

from symantec_package.lib.managementService.SymantecManagementServices import SymantecManagementServices

from symantec_package.HTTPHandler import setConnection, HTTPSClientAuthHandler, HTTPSClientCertTransport


class TestUserManagement(unittest.TestCase):
    def setUp(self):
        # the URLs for now which will have the WSDL files and the XSD file
        query_services_url = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
        userservices_url = 'http://webdev.cse.msu.edu/~morcoteg/Symantec/WSDL/vipuserservices-auth-1.7.wsdl'
        managementservices_url = 'http://webdev.cse.msu.edu/~huynhall/vipuserservices-mgmt-1.7.wsdl'

        # initializing the Suds clients for each url, with the client certificate youll have in the same dir as this file
        self.management_client = Client(managementservices_url,
                                        transport=HTTPSClientCertTransport('vip_certificate.crt',
                                                                           'vip_certificate.crt'))

        self.test_management_services_object = SymantecManagementServices(self.management_client)
        pass


    @patch('symantec_package.lib.managementService.SymantecManagementServices')
    def test_mock_create_user(self, mock_managementservices):
        reply = \
        """<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
           <S:Body>
              <CreateUserResponse xmlns="https://schemas.symantec.com/vip/2011/04/vipuserservices">
                 <requestId>create_123</requestId>
                 <status>0000</status>
                 <statusMessage>Success</statusMessage>
              </CreateUserResponse>
           </S:Body>
        </S:Envelope>
        """
        # Configure the mock to return a response with an OK status code. Also, the mock should have
        # a `json()` method that returns a list of todos.
        mock_managementservices.createUser.return_value = Mock()
        mock_managementservices.createUser.return_value.json.return_value = reply

        # Call the service, which will send a request to the server.
        response = symantec_package.lib.managementService.SymantecManagementServices.createUser("create_123",
                                                                                                "new_user3")

        print(response.json())
        # If the request is sent successfully, then I expect a response to be returned.
        self.assertTrue(str(response.json()) == reply)
        pass

    @patch('symantec_package.lib.managementService.SymantecManagementServices')
    def test_mock_delete_user(self, mock_managementservices):
        reply = \
        """<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
           <S:Body>
              <DeleteUserResponse xmlns="https://schemas.symantec.com/vip/2011/04/vipuserservices">
                 <requestId>delete_123</requestId>
                 <status>0000</status>
                 <statusMessage>Success</statusMessage>
              </DeleteUserResponse>
           </S:Body>
        </S:Envelope>
        """
        # Configure the mock to return a response with an OK status code. Also, the mock should have
        # a `json()` method that returns a list of todos.
        mock_managementservices.deleteUser.return_value = Mock()
        mock_managementservices.deleteUser.return_value.json.return_value = reply

        # Call the service, which will send a request to the server.
        response = symantec_package.lib.managementService.SymantecManagementServices.deleteUser("delete_123",
                                                                                                "new_user3")

        print(response.json())
        # If the request is sent successfully, then I expect a response to be returned.
        self.assertTrue(str(response.json()) == reply)
        pass

        @patch('symantec_package.lib.managementService.SymantecManagementServices')
        def test_mock_add_STANDARDOTP_credential(self, mock_managementservices):

            pass

        # def test_add_and_delete_STANDARD_OTP_credential(self):
        #     user = self.test_management_services_object.createUser("new_user456", "new_user3")
        #     self.assertTrue("0000" in str(user))
        #
        #     otp_credential = self.test_management_services_object.addCredential("new_otp_cred", "new_user3", "VSTZ39646177", "STANDARD_OTP",\
        #                                                                         "672192")       #change with what's on your device
        #     self.assertTrue("0000" in str(otp_credential))
        #
        #     deleted = self.test_management_services_object.removeCredential("remove_123", "new_user3", "VSTZ39646177",
        #                                                                     "STANDARD_OTP")
        #     self.assertTrue("0000" in str(deleted))
        #
        #     user = self.test_management_services_object.deleteUser("delete_user123", "new_user3")
        #     self.assertTrue("0000" in str(user))
        #     pass


if __name__ == '__main__':
    unittest.main()