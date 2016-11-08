import urllib.request, http.client, socket
from suds.client import Client
from suds.transport.http import HttpTransport, Reply, TransportError


class HTTPSClientAuthHandler(urllib.request.HTTPSHandler):
    def __init__(self, key, cert):
        urllib.request.HTTPSHandler.__init__(self)
        self.key = key
        self.cert = cert

    def https_open(self, req):
        #Rather than pass in a reference to a connection class, we pass in
        # a reference to a function which, for all intents and purposes,
        # will behave as a constructor
        return self.do_open(self.getConnection, req)

    def getConnection(self, host, timeout=300):
        return http.client.HTTPSConnection(host,
                                       key_file=self.key,
                                       cert_file=self.cert)

class HTTPSClientCertTransport(HttpTransport):
    def __init__(self, key, cert, *args, **kwargs):
        HttpTransport.__init__(self, *args, **kwargs)
        self.key = key
        self.cert = cert

    def u2open(self, u2request):
        """
        Open a connection.
        @param u2request: A urllib2 request.
        @type u2request: urllib2.Requet.
        @return: The opened file-like urllib2 object.
        @rtype: fp
        """
        tm = self.options.timeout
        url = urllib.request.build_opener(HTTPSClientAuthHandler(self.key, self.cert))
        if self.u2ver() < 2.6:
            socket.setdefaulttimeout(tm)
            return url.open(u2request)
        else:
            return url.open(u2request, timeout=tm)



import logging
import sys
sys.path.append("/home/oem/PycharmProjects/Securitas_Dev/Securitas")
from symantec_package.lib.userService.SymantecUserServices import SymantecUserServices
from symantec_package.lib.queryService.SymantecQueryServices import SymantecQueryServices
from symantec_package.lib.managementService.SymantecManagementServices import SymantecManagementServices
from symantec_package.lib.allServices.SymantecServices import SymantecServices

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

from suds.client import Client
#from suds.transport.https import


# the URLs for now which will have the WSDL files and the XSD file
query_services_url = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
userservices_url = 'http://webdev.cse.msu.edu/~morcoteg/Symantec/WSDL/vipuserservices-auth-1.4.wsdl'
managementservices_url = 'http://webdev.cse.msu.edu/~huynhall/vipuserservices-mgmt-1.7.wsdl'

# initializing the Suds clients for each url, with the client certificate youll have in the same dir as this file
query_services_client = Client(query_services_url,
         transport = HTTPSClientCertTransport('vip_certificate.crt','vip_certificate.crt'))
user_services_client = Client(userservices_url,
         transport = HTTPSClientCertTransport('vip_certificate.crt','vip_certificate.crt'))
management_client = Client(managementservices_url,
         transport = HTTPSClientCertTransport('vip_certificate.crt','vip_certificate.crt'))

#get_user_info_result = query_services_client.service.getUserInfo(requestId="123123", userId="y1196293")

test_user_services_object = SymantecUserServices(user_services_client)
test_query_services_object = SymantecQueryServices(query_services_client)
test_management_services_object = SymantecManagementServices(management_client)
test_services = SymantecServices(query_services_client, management_client, user_services_client)

#send_push_to_phone_result = test_user_services_object.authenticateUserWithPush("push_123", "gabe_phone")
#print(test_user_services_object.__str__("push_123", "gabe_phone"))

#print(user_services_client)
# authenticate_result = test_user_services_object.authenticateCredentials("push_456", \
#                                                                         {"credentialId": "VSTZ39646177", "credentialType": "STANDARD_OTP"}, \
#                                                                         {"otp": "263881"})
#a_result = test_user_services_object.authenticateWithStandard_OTP("push_123", "VSTZ39646177", input("\nEnter 6-digit security code: "))
#transaction_id = test_user_services_object.getFieldContent('transactionId')
#polling = test_query_services_object.pollPushStatus("push_456", transaction_id)
#print(test_user_services_object.__str__("push_456", "gabe_phone"))



#print(str(get_user_info_result).split('\n'))

#*****************************ALLEN TESTS

### SMS test
# user_id = input("\nEnter User ID: ")
# phoneNumber = input("Enter phone number: ")
# send_SMS = test_management_services_object.sendOtpSMS("SMS_Test", user_id, phoneNumber)
# print (send_SMS)
#
# results_SMS = test_user_services_object.authenticateWithSMS("SMS_Result_Test", phoneNumber, input("\nEnter Security Code: "))
# print (results_SMS)


testy = test_query_services_object.getUserInfo("Test12", "Arren_phone")
# print((testy))
# print(testy['credentialBindingDetail'])
# print(testy['credentialBindingDetail'][1]['credentialId'])
# for key in testy:
#     print(key)
#     for value in key:
#         print(value)

testTime = test_query_services_object.getServerTime("timers")
print(testTime.index("requestId"))

# # test new encompassing class
#services_push = test_services.authenticateUserWithPush("push_123", "Arren_phone")
# test_services.authenticateUserWithPushThenPolling( "Push_Test", "PushPollTest","Arren_phone")