#!/usr/bin/env python
# -*- coding: utf-8 -*-#
#
#
# Copyright (c) 2019 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
import unittest
from oauth1.oauth import OAuth
from oauth1.oauth import OAuthParameters
import oauth1.authenticationutils as authenticationutils
import oauth1.coreutils as Util
from os.path import dirname, realpath, join

from oauth1.signer import OAuthSigner



class OAuthTest(unittest.TestCase):

    signing_key = authenticationutils.load_signing_key("./fake-key.p12", "fakepassword")
    consumer_key = OAuthSigner("uLXKmWNmIkzIGKfA2injnNQqpZaxaBSKxa3ixEVu2f283c95!33b9b2bd960147e387fa6f3f238f07170000000000000000", signing_key)

    def test_get_authorization_header(self):
        uri = "https://sandbox.api.mastercard.com/fraud/merchant/v1/termination-inquiry?Format=XML&PageOffset=0"
        method = "POST"
        header = OAuth().get_authorization_header(uri, method, "payload", self.consumer_key, self.signing_key)


    def test_get_nonce(self):
        nonce = OAuth.get_nonce()
        self.assertEqual(len(nonce),16)

    def test_get_timestamp(self):
        timestamp = OAuth.get_timestamp()
        self.assertEqual(len(str(timestamp)),10)

    def test_sign_message(self):

        baseString = 'POST&https%3A%2F%2Fsandbox.api.mastercard.com%2Ffraud%2Fmerchant%2Fv1%2Ftermination-inquiry&Format%3DXML%26PageLength%3D10%26PageOffset%3D0%26oauth_body_hash%3DWhqqH%252BTU95VgZMItpdq78BWb4cE%253D%26oauth_consumer_key%3Dxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx%26oauth_nonce%3D1111111111111111111%26oauth_signature_method%3DRSA-SHA1%26oauth_timestamp%3D1111111111%26oauth_version%3D1.0'

        signature = OAuth().sign_message(baseString, self.signing_key)

        signature = Util.uri_rfc3986_encode(signature)

        self.assertEqual(signature,"nqxpgHpye%2BdOEkEbC%2FS3N1%2FCRFlZPHoyRztkRhkCoz7ISNmV9V60TQ7zwS8Q59SGQUGYuoNSVe8SWtNVQTEuRiZfXd6Eme%2BCdHfAt7%2BbNd3UsrcIHl3CJEvx7u70ItW8aOx4F7rjF%2BaIOq%2Bpc0rbuBugF%2BnElGKydpPiQrKKwE5kB3TZKVkYLLCsLU8Ry%2Fjg05d2TcnGTyfYZDchV4ui0uPzR5UH%2Fkb4ni8lchrtAeaGJwCimACIk6qNLoNnz7u9joKHtYeuZhORRVodxKB%2BAolgAQqJBMyLrseJDITmwIRTRSzQ3vclt%2BMvVs1CMbXYuvnDYd5NFv98emJgBC%2FX1A%3D%3D")


    def test_oauth_parameters(self):
        uri = "https://sandbox.api.mastercard.com/fraud/merchant/v1/termination-inquiry?Format=XML&PageOffset=0"
        method = "POST"
        parameters = OAuth().get_oauth_parameters(uri, method, "payload", self.consumer_key, self.signing_key)
        # print(parameters)
        consumer_key = parameters.get_oauth_consumer_key()
        

    def test_query_parser(self):
        uri = "https://sandbox.api.mastercard.com/audiences/v1/getcountries?offset=0&offset=1&length=10&empty&odd="

        oauth_parameters = OAuthParameters()
        oauth_parameters_base = oauth_parameters.get_base_parameters_dict()
        merge_parameters = oauth_parameters_base.copy()
        query_params = Util.normalize_params(uri, merge_parameters)
        # print(query_params)
        self.assertEqual(query_params, "empty=&length=10&odd=&offset=0&offset=1")
        # - length=10&offset=1
        # + empty&length=10&odd=&offset=0&offset=1
        



    def test_query_parser_encoding(self):
        uri = "https://sandbox.api.mastercard.com?param1=plus+value&param2=colon:value"

        oauth_parameters = OAuthParameters()
        oauth_parameters_base = oauth_parameters.get_base_parameters_dict()
        merge_parameters = oauth_parameters_base.copy()
        query_params = Util.normalize_params(uri, merge_parameters)
        # print(query_params)
        self.assertEqual(query_params, "param1=plus%2Bvalue&param2=colon%3Avalue")


    def test_query_parser_not_encoded_params(self):
        uri = "https://api.mastercard.com/audiences?param1=plus+value&param2=colon:value&param3=a space~"

        oauth_parameters = OAuthParameters()
        oauth_parameters_base = oauth_parameters.get_base_parameters_dict()
        merge_parameters = oauth_parameters_base.copy()
        query_params = Util.normalize_params(uri, merge_parameters)
        print(query_params)
        self.assertEqual(query_params, "param1=plus%20value&param2=colon%3Avalue&param3=a%20space~")
        # - param1=plus%2Bvalue&param2=colon%3Avalue&param3=a%2Bspace~
        # + param1=plus%2Bvalue&param2=colon%3Avalue&param3=a%20space~


    def test_nonce_length(self):
        nonce = OAuth.get_nonce()
        self.assertEqual(16, len(nonce))

    def test_nonce_uniqueness(self):
        init = OAuth.get_nonce()
        l = []
        for i  in range(0,100000):
            l.append(init +  OAuth.get_nonce() )
            
        # print(*l)
        # print(self.list_duplicates(l))
        self.assertEqual(self.list_duplicates(l), [])


    def list_duplicates(self, seq):
        seen = set()
        seen_add = seen.add
        # adds all elements it doesn't know yet to seen and all other to seen_twice
        seen_twice = set( x for x in seq if x in seen or seen_add(x) )
        # turn the set into a list (as requested)
        return list( seen_twice )


    def test_params_string_rfc_example_1(self):
        uri = "https://sandbox.api.mastercard.com"
        # uri = "b5=%3D%253D&a3=a&a3=2%20q&c%40=&a2=r%20b&c2="

        oauth_parameters1 = OAuthParameters()
        oauth_parameters1.set_oauth_consumer_key("9djdj82h48djs9d2")
        oauth_parameters1.set_oauth_signature_method("HMAC-SHA1")
        oauth_parameters1.set_oauth_timestamp("137131201")
        oauth_parameters1.set_oauth_nonce("7d8f3e4a")

        oauth_parameters_base1 = oauth_parameters1.get_base_parameters_dict()
        merge_parameters1 = oauth_parameters_base1.copy()
        query_params1 = Util.normalize_params(uri, merge_parameters1)

        self.assertEqual("oauth_consumer_key=9djdj82h48djs9d2&oauth_nonce=7d8f3e4a&oauth_signature_method=HMAC-SHA1&oauth_timestamp=137131201", query_params1);


    def test_params_string_rfc_example_2(self):
        uri = "https://sandbox.api.mastercard.com?b5=%3D%253D&a3=a&a3=2%20q&c%40=&a2=r%20b&c2="

        oauth_parameters2 = OAuthParameters()
        oauth_parameters_base2 = oauth_parameters2.get_base_parameters_dict()
        merge_parameters2 = oauth_parameters_base2.copy()
        query_params2 = Util.normalize_params(uri, merge_parameters2)

        self.assertEqual("a2=r%20b&a3=2%20q&a3=a&b5=%3D%253D&c%40=&c2=", query_params2)
        # - a2=r%20b&a3=2%20q&a3=a&b5=%3D%253D&c%40=&c2=
        # + a2=r%2Bb&a3=2%2Bq&b5=%3D%253D
        



    def test_params_string_ascending_byte_value_ordering(self):
        print("FIXME")
        url = "https://localhost?b=b&A=a&A=A&B=B&a=A&a=a&0=0"

        oauth_parameters = OAuthParameters()
        oauth_parameters_base = oauth_parameters.get_base_parameters_dict()
        merge_parameters = oauth_parameters_base.copy()
        norm_params = Util.normalize_params(url, merge_parameters)
        print("bbbbXXXXXXXXXXXXX")
        print(norm_params)
        print("bbbbXXXXXXXXXXXXX")

        self.assertEqual("0=0&A=A&A=a&B=B&a=A&a=a&b=b", norm_params)
        # - 0=0&A=A&A=a&B=B&a=A&a=a&b=b
        # ?         ----   ----
        # + 0=0&A=A&B=B&a=a&b=b



    def test_signature_base_string(self):
        print("FIXME")
        uri = "https://api.mastercard.com"
        base_uri = Util.normalize_url(uri)

        oauth_parameters = OAuthParameters()
        oauth_parameters.set_oauth_body_hash("body/hash")
        oauth_parameters.set_oauth_nonce("randomnonce")

        base_string = OAuth.get_base_string(base_uri, "POST", oauth_parameters, oauth_parameters.get_base_parameters_dict())
        print(base_string)

        self.assertEqual("POST&https%3A%2F%2Fapi.mastercard.com&oauth_body_hash%3Dbody%2Fhash%26oauth_nonce%3Drandomnonce", base_string);
        # - POST&https%3A%2F%2Fapi.mastercard.com&oauth_body_hash%3Dbody%2Fhash%26oauth_nonce%3Drandomnonce
        # + POST&https%3A%2F%2Fapi.mastercard.com%2F&oauth_body_hash%3Dbody%252Fhash%26oauth_nonce%3Drandomnonce
        

        
    def test_signature_base_string2(self):
        print("FIXME")
        body = "<?xml version=\"1.0\" encoding=\"Windows-1252\"?><ns2:TerminationInquiryRequest xmlns:ns2=\"http://mastercard.com/termination\"><AcquirerId>1996</AcquirerId><TransactionReferenceNumber>1</TransactionReferenceNumber><Merchant><Name>TEST</Name><DoingBusinessAsName>TEST</DoingBusinessAsName><PhoneNumber>5555555555</PhoneNumber><NationalTaxId>1234567890</NationalTaxId><Address><Line1>5555 Test Lane</Line1><City>TEST</City><CountrySubdivision>XX</CountrySubdivision><PostalCode>12345</PostalCode><Country>USA</Country></Address><Principal><FirstName>John</FirstName><LastName>Smith</LastName><NationalId>1234567890</NationalId><PhoneNumber>5555555555</PhoneNumber><Address><Line1>5555 Test Lane</Line1><City>TEST</City><CountrySubdivision>XX</CountrySubdivision><PostalCode>12345</PostalCode><Country>USA</Country></Address><DriversLicense><Number>1234567890</Number><CountrySubdivision>XX</CountrySubdivision></DriversLicense></Principal></Merchant></ns2:TerminationInquiryRequest>";
        url = "https://sandbox.api.mastercard.com/fraud/merchant/v1/termination-inquiry?Format=XML&PageOffset=0&PageLength=10"
        method = "POST"

        oauth_parameters = OAuthParameters()
        oauth_parameters.set_oauth_consumer_key("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        oauth_parameters.set_oauth_nonce("1111111111111111111")
        oauth_parameters.set_oauth_timestamp("1111111111")
        oauth_parameters.set_oauth_version("1.0")
        oauth_parameters.set_oauth_body_hash("body/hash")
        encoded_hash = Util.base64_encode(Util.sha256_encode(body))
        oauth_parameters.set_oauth_body_hash(encoded_hash)

        oauth_parameters_base = oauth_parameters.get_base_parameters_dict()
        merge_parameters = oauth_parameters_base.copy()


        norm_params = Util.normalize_params("", merge_parameters)
        print("XXXXXXXXXXXXX")
        # print(oauth_parameters_base)
        print(norm_params)

        query_params = OAuth.get_query_params(url)
        
        print("YYYYYXXXXXXXXXXXXX")
        # print(query_params)
        normalize_params = Util.normalize_params("", query_params)
        print(normalize_params)

        base_string = OAuth.get_base_string(url, method, oauth_parameters, oauth_parameters.get_base_parameters_dict())
        print(base_string)

        expected = "POST&https%3A%2F%2Fsandbox.api.mastercard.com%2Ffraud%2Fmerchant%2Fv1%2Ftermination-inquiry&Format%3DXML%26PageLength%3D10%26PageOffset%3D0%26oauth_body_hash%3Dh2Pd7zlzEZjZVIKB4j94UZn%2FxxoR3RoCjYQ9%2FJdadGQ%3D%26oauth_consumer_key%3Dxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx%26oauth_nonce%3D1111111111111111111%26oauth_timestamp%3D1111111111%26oauth_version%3D1.0"

        self.maxDiff = None
        self.assertEqual(expected, base_string);
        # - POST&https%3A%2F%2Fsandbox.api.mastercard.com%2Ffraud%2Fmerchant%2Fv1%2Ftermination-inquiry&Format%3DXML%26PageLength%3D10%26PageOffset%3D0%26oauth_body_hash%3Dh2Pd7zlzEZjZVIKB4j94UZn%2FxxoR3RoCjYQ9%2FJdadGQ%3D%26oauth_consumer_key%3Dxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx%26oauth_nonce%3D1111111111111111111%26oauth_timestamp%3D1111111111%26oauth_version%3D1.0
        # + POST&https%3A%2F%2Fsandbox.api.mastercard.com%2Ffraud%2Fmerchant%2Fv1%2Ftermination-inquiry&Format%3DXML%26PageLength%3D10%26PageOffset%3D0%26oauth_body_hash%3Dh2Pd7zlzEZjZVIKB4j94UZn%252FxxoR3RoCjYQ9%252FJdadGQ%253D%26oauth_consumer_key%3Dxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx%26oauth_nonce%3D1111111111111111111%26oauth_timestamp%3D1111111111%26oauth_version%3D1.0

        
        
    def test_sign_signature_base_string_invalid_key(self):
        self.assertRaises(AttributeError, OAuth.sign_message, self, "some string", None)        
        
        
    def test_sign_signature_base_string(self):
        # expectedSignatureString = "IJeNKYGfUhFtj5OAPRI92uwfjJJLCej3RCMLbp7R6OIYJhtwxnTkloHQ2bgV7fks4GT/A7rkqrgUGk0ewbwIC6nS3piJHyKVc7rvQXZuCQeeeQpFzLRiH3rsb+ZS+AULK+jzDje4Fb+BQR6XmxuuJmY6YrAKkj13Ln4K6bZJlSxOizbNvt+Htnx+hNd4VgaVBeJKcLhHfZbWQxK76nMnjY7nDcM/2R6LUIR2oLG1L9m55WP3bakAvmOr392ulv1+mWCwDAZZzQ4lakDD2BTu0ZaVsvBW+mcKFxYeTq7SyTQMM4lEwFPJ6RLc8jJJ+veJXHekLVzWg4qHRtzNBLz1mA=="
        expectedSignatureString = "vA7b0GT6r3GrS7Zpvy7PDMKocmG79yvpnp77GK8znpTKcY9xwKP5n4BfoP26068TyIZk9qx5TEzc4FzOKhWZF5pxN77Hne0A7gHNkaueYmfy95qxUBxLRMCevwjs5A0aW1bTW+gu7VL1cLtBYgO9Ks2axUcvxAq6aVRZvMGvFukxaZd+2XD8hE/tBwyEmvQwWO9gr5KJAFslkykjID9zs4gZ+gK0adRCvpcobRfcff+RxbtQctq3cjXwH/Fp3ZymoFtB2J+4hJ3aX4uCkIhJCV4dyWUkvx81vNyf1J5nBjqRtAoOEXOxNrz4o+kzAfcT46EUSQUTjouCO6hJfOVlaA=="
        signing_string = OAuth.sign_message(self, "baseString", self.signing_key)
        self.maxDiff = None
        self.assertEqual(expectedSignatureString, signing_string)
        

    def test_url_normalization_rfc_examples1(self):
        uri = "https://www.example.net:8080"
        base_uri = Util.normalize_url(uri)
        self.assertEqual("https://www.example.net:8080/", base_uri)

    def test_url_normalization_rfc_examples2(self):
        uri = "http://EXAMPLE.COM:80/r%20v/X?id=123"
        base_uri = Util.normalize_url(uri)
        self.assertEqual("http://example.com/r%20v/X", base_uri);
        
    def test_url_normalization_redundant_ports1(self):
        uri = "https://api.mastercard.com:443/test?query=param"
        base_uri = Util.normalize_url(uri)
        self.assertEqual("https://api.mastercard.com/test", base_uri)

    def test_url_normalization_redundant_ports2(self):
        uri = "http://api.mastercard.com:80/test"
        base_uri = Util.normalize_url(uri)
        self.assertEqual("http://api.mastercard.com/test", base_uri)

    def test_url_normalization_redundant_ports3(self):
        uri = "https://api.mastercard.com:17443/test?query=param"
        base_uri = Util.normalize_url(uri)
        self.assertEqual("https://api.mastercard.com:17443/test", base_uri)


    def test_url_normalization_remove_fragment(self):
        uri = "https://api.mastercard.com/test?query=param#fragment"
        base_uri = Util.normalize_url(uri)
        self.assertEqual("https://api.mastercard.com/test", base_uri);


    def test_url_normalization_add_trailing_slash(self):
        uri = "https://api.mastercard.com"
        base_uri = Util.normalize_url(uri)
        self.assertEqual("https://api.mastercard.com/", base_uri);


    def test_url_normalization_lowercase_scheme_and_host(self):
        uri = "HTTPS://API.MASTERCARD.COM/TEST"
        base_uri = Util.normalize_url(uri)
        self.assertEqual("https://api.mastercard.com/TEST", base_uri)


    def test_body_hash1(self):
        oauth_parameters = OAuthParameters()
        encoded_hash = Util.base64_encode(Util.sha256_encode(OAuth.EMPTY_STRING))
        # print(encoded_hash)
        oauth_parameters.set_oauth_body_hash(encoded_hash)
        self.assertEqual("47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=", encoded_hash)

    def test_body_hash2(self):
        oauth_parameters = OAuthParameters()
        encoded_hash = Util.base64_encode(Util.sha256_encode(None))
        # print(encoded_hash)
        oauth_parameters.set_oauth_body_hash(encoded_hash)
        self.assertEqual("3JN7WYkmBPWoaslpNs1/8J4l8Yrmt1joAUokx/oDnpE=", encoded_hash)

    def test_body_hash3(self):
        oauth_parameters = OAuthParameters()
        encoded_hash = Util.base64_encode(Util.sha256_encode("{\"foõ\":\"bar\"}"))
        # print(encoded_hash)
        oauth_parameters.set_oauth_body_hash(encoded_hash)
        self.assertEqual("+Z+PWW2TJDnPvRcTgol+nKO3LT7xm8smnsg+//XMIyI=", encoded_hash)


    # NOT NEEDED - INTERNAL
    #   @Test(expected = IllegalStateException.class)
    #   public void bodyHash_invalidHashAlgorithm() {
    #     OAuth.getBodyHash(OAuth.EMPTY_STRING, UTF8_CHARSET, "SHA-123");
    #   }


    def test_url_encode1(self):
        self.assertEqual("Format%3DXML", Util.uri_rfc3986_encode("Format=XML"))

    def test_url_encode2(self):
        self.assertEqual("WhqqH%2BTU95VgZMItpdq78BWb4cE%3D", Util.uri_rfc3986_encode("WhqqH+TU95VgZMItpdq78BWb4cE="))
    def test_url_encode3(self):
        self.assertEqual("WhqqH%2BTU95VgZMItpdq78BWb4cE%3D%26o", Util.uri_rfc3986_encode("WhqqH+TU95VgZMItpdq78BWb4cE=&o"))
        # Tilde stays unescaped - really?
        # self.assertEqual("WhqqH%2BTU95VgZ~Itpdq78BWb4cE%3D%26o", Util.uri_rfc3986_encode("WhqqH+TU95VgZ~Itpdq78BWb4cE=&o"))


        
if __name__ == '__main__':
    unittest.main()
