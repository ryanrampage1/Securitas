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
from symantec_package.lib.userService.SymantecUserServices import SymantecUserServices
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

from suds.client import Client
#from suds.transport.https import


# the URLs for now which will have the WSDL files and the XSD file
url = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
userservices_url = 'http://webdev.cse.msu.edu/~morcoteg/Symantec/WSDL/vipuserservices-auth-1.4.wsdl'
managementservices_url = 'http://webdev.cse.msu.edu/~huynhall/vipuserservices-mgmt-1.7.wsdl'

# initializing the Suds clients for each url, with the client certificate youll have in the same dir as this file
client = Client(url,
         transport = HTTPSClientCertTransport('vip_certificate.crt','vip_certificate.crt'))
user_services_client = Client(userservices_url,
         transport = HTTPSClientCertTransport('vip_certificate.crt','vip_certificate.crt'))
management_client = Client(managementservices_url,
         transport = HTTPSClientCertTransport('vip_certificate.crt','vip_certificate.crt'))
# get_user_info_result = client.service.getUserInfo(requestId="123123", userId="y1196293")
# print(get_user_info_result)

# Bunch of Allen query tests
# get_server_time = client.service.getServerTime(requestId="server123")
# print(get_server_time)
# get_credential_info = client.service.getCredentialInfo(requestId="credential123", onBehalfOfAccountId=None,
#                                                        credentialId="VSTZ43724471", credentialType="STANDARD_OTP")
# print(get_credential_info)
# get_temp_pass_attributes = client.service.getTemporaryPasswordAttributes(requestId="temp_pass",
#                                                                          onBehalfOfAccountId=None, userId="Arren_phone")
# print(get_temp_pass_attributes)
# get_poll_push_status = client.service.pollPushStatus(requestId="poll_test",onBehalfOfAccountId=None, transactionId="123321")
# print(get_poll_push_status)

#test_user_services_object = SymantecUserServices(user_services_client)
# send_push_to_phone_result = test_user_services_object.authenticateUserWithPush("push_123", "Arren_phone")
# print(test_user_services_object.__str__("push_123", "Arren_phone"))
# resp = test_user_services_object.__str__("push_123", "Arren_phone")
# info_list = resp.split('\n')
# import time
# for item in info_list:
#     if "transactionId" in item:
#         ID = item.split('=')[1][1:].strip('"')
#         # JUST FOR TESTING DO NOT use sleep in final code unless on another thread
#         for poll in range(1,6): #polls every 5 seconds up til 30 seconds
#             time.sleep(5)
#             get_poll_push_status = str(client.service.pollPushStatus(requestId="poll_test",onBehalfOfAccountId=None, transactionId=ID))
#             #print(get_poll_push_status)
#             # need to check response for transaction status
#             lines = get_poll_push_status.split('\n')
#             for l in lines:
#                 if "7000" in l:
#                     print(get_poll_push_status)
#                     break
#         break


### some SMS stuff
send_SMS = management_client.service.sendOtp(requestId="SMS_Arren", userId="Arren_phone", smsDeliveryInfo={"phoneNumber": "16167803665"})
print(send_SMS)

##########
# Gabe here, testing pushing to phone with wrapper class SymantecUserServices
#test_user_services_object = SymantecUserServices(user_services_client)
#send_push_to_phone_result = test_user_services_object.authenticateUserWithPush("push_123", "Arren_phone")
#print(test_user_services_object.__str__("push_123", "Arren_phone"))


#print(str(get_user_info_result).split('\n'))