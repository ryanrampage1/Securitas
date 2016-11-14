"""
.. module:: SymantecLegacyService
    :platform: All platforms that are compatible with Python framework
    :synopsis: Module handles other useful VIP SOAP calls

.. moduleauthor:: Allen Huynh

"""

class SymantecLegacyServices:
    """This class acts as a layer of abstraction to handling Symantec VIP SOAP calls in Python.

    You call this class to handle to managing users and credentials using authentication API.

    Example:
        >>> client = Client("http://../vip_auth.wsdl", transport = HTTPSClientCertTransport('vip_certificate.crt','vip_certificate.crt'))
        >>> service = SymantecLegacyServices(client)
        >>> response = service.sendOtpSMS(<parameters here>)
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
        self.response = None

    # NOTE: NEED TO FIX SO THAT <TokenId type="SMS">
    def setTemporaryPassword(self, credentialId, password, expirationDate=None, oneTimeUseOnly=None):
        res = self.client.service.setTemporaryPassword(TokenId=credentialId, TemporaryPassword=password, ExpirationDate=
                                                       expirationDate, OneTimeUseOnly=oneTimeUseOnly)
        self.response = res
        return res

    # NOTE: NEED TO FIX SO THAT <TokenId type="SMS">
    def sendOtpSmsUsingCredentialId(self, credentialId, authorizerAccountId=None,SMSFrom=None, message=None):
        if SMSFrom is None and message is None:
            res = self.client.service.SendOtp(AuthorizerAccountId=authorizerAccountId, TokenId=credentialId,
                                              SMSDeliveryInfo=None, VoiceDeliveryInfo=None)
        elif SMSFrom is None and message is not None:
            res = self.client.service.SendOtp(AuthorizerAccountId=authorizerAccountId, TokenId=credentialId,
                                              SMSDeliveryInfo={"Message": message}, VoiceDeliveryInfo=None)
        elif SMSFrom is not None and message is None:
            res = self.client.service.SendOtp(AuthorizerAccountId=authorizerAccountId, TokenId=credentialId,
                                              SMSDeliveryInfo={"SMSFrom": SMSFrom}, VoiceDeliveryInfo=None)
        else:
            res = self.client.service.SendOtp(AuthorizerAccountId=authorizerAccountId, TokenId=credentialId,
                                              SMSDeliveryInfo={"SMSFrom": SMSFrom, "Message":message}, VoiceDeliveryInfo=None)
        self.response = res
        return res

    # NOTE: NEED TO FIX SO THAT <TokenId type="SMS">
    def enableCredentialSMS(self, credentialId, authorizerAccountId=None):
        res = self.client.service.EnableToken(AuthorizerAccountId=authorizerAccountId, TokenId=credentialId)
        self.response = res
        return res
    # same here
    def activateCredentialSMS(self):
        return self.response
    # NOTE: NEED TO FIX SO THAT <TokenId type="SMS">
    def disableCredentialSMS(self):
        return self.response
    # same here
    def deactivateCredentialSMS(self):
        return self.response

    def getFieldContent(self, fieldname):
        """

            :description: *Get content of items in response message*
            :note: Works only for one line item
            :param fieldname: Item name
            :type fieldname: string
            :returns: The content of input fieldname

        """
        info_list = self.__str__().split('\n')

        for item in info_list:
            if fieldname in item:
                return item.split('=')[1][1:]

        pass


    # iterates through first level of main response fields from previous SOAP call and tells what fields are accessible
    # gives warning if that field is a list containing more sub-fields
    def getPreviousResponseFirstPairs(self):
        """

            :description: *Gets the 1st level of important main response fields from previous VIP SOAP call and tells what fields are accessible*
            :note: This will not work if there was no previous call in the client.
            :returns: list -- Containing all the first pair values of each tuple

        """
        # list to hold first pair value in tuples
        firstPairs = []
        warnings = []
        index = 0
        # NOTE: SOAP response is similar to tuples and dictionaries but are not of those types.
        for tup in self.response:
            # tup[0] #first of pair (key)
            # tup[1] #second of pair (value)

            # WE check for list
            if type(tup[1]) is list:
                warning = "WARNING: '" + str(tup[0]) + "' at " + "index(" + str(index) + ") is a list!!!"
                print(warning)
                warnings.append(warning)
            firstPairs.append(str(tup[0]))
            index += 1
        return firstPairs


    # iterates through first level of main response fields and tells what fields are accessible
    # gives warning if that field is a list containing more sub-fields
    def getResponseFirstPairs(self, response):
        """

            :description: *Gets the 1st level of important main response fields from the VIP SOAP call and tells what fields are accessible*
            :note: This requires the SOAP response as a parameter.
            :param response: The SOAP response
            :type response: list of tuples
            :returns: list -- Containing all the first pair values of each tuple

        """
        # list to hold first pair value in tuples
        firstPairs = []
        warnings = []
        index = 0
        # NOTE: SOAP response is similar to tuples and dictionaries but are not of those types.
        for tup in response:
            # tup[0] #first of pair (key)
            # tup[1] #second of pair (value)

            # WE check for list
            if type(tup[1]) is list:
                warning = "WARNING: '" + str(tup[0]) + "' at " + "index(" + str(index) + ") is a list!!!"
                print(warning)
                warnings.append(warning)
            firstPairs.append(str(tup[0]))
            index += 1
        return firstPairs


    # Returns the field value at that key of the pair; this uses the previous response
    def getPreviousResponseValue(self, firstPair):
        """

            :description: *Gets the 1st level of important main response fields from the VIP SOAP call and tells what fields are accessible*
            :note: This will not work if there was no previous call in the client.
            :param firstPair: The first pair in the tuple field
            :type firstPair: string
            :returns: The field value at the pair key

        """
        return self.response[firstPair]


    # Returns the field value at that key of the pair
    def getResponseValue(self, response, firstPair):
        """

            :description: *Gets the 1st level of important main response fields from the VIP SOAP call and tells what fields are accessible*
            :note: This requires the SOAP response as a parameter.
            :param response: The SOAP response
            :type response: list of tuples
            :param firstPair: The first pair in the tuple field
            :type firstPair: string
            :returns: The field value at the pair key

        """
        return response[firstPair]