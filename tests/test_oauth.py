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
import oauth1.authenticationutils as authenticationutils
import oauth1.coreutils as Util
from os.path import dirname, realpath, join

from oauth1.signer import OAuthSigner


class OAuthTest(unittest.TestCase):

    keyFile = join(dirname(dirname(realpath(__file__))),"tests","fake-key.p12")
    signing_key = authenticationutils.load_signing_key(keyFile, "fakepassword")
    consumer_key = OAuthSigner("uLXKmWNmIkzIGKfA2injnNQqpZaxaBSKxa3ixEVu2f283c95!33b9b2bd960147e387fa6f3f238f07170000000000000000", signing_key)

    def test_get_authorization_header(self):
        uri = "https://sandbox.api.mastercard.com/fraud/merchant/v1/termination-inquiry?Format=XML&PageOffset=0"
        method = "POST"
        header = OAuth.get_authorization_header(self, uri, method, "payload", self.consumer_key, self.signing_key)



    def test_get_nonce(self):
        nonce = OAuth.get_nonce()
        self.assertEqual(len(nonce),16)

    def test_get_timestamp(self):
        timestamp = OAuth.get_timestamp()
        self.assertEqual(len(str(timestamp)),10)

    def test_sign_message(self):

        baseString = 'POST&https%3A%2F%2Fsandbox.api.mastercard.com%2Ffraud%2Fmerchant%2Fv1%2Ftermination-inquiry&Format%3DXML%26PageLength%3D10%26PageOffset%3D0%26oauth_body_hash%3DWhqqH%252BTU95VgZMItpdq78BWb4cE%253D%26oauth_consumer_key%3Dxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx%26oauth_nonce%3D1111111111111111111%26oauth_signature_method%3DRSA-SHA1%26oauth_timestamp%3D1111111111%26oauth_version%3D1.0'

        signature = OAuth.sign_message(self, baseString, self.signing_key)

        signature = Util.uri_rfc3986_encode(signature)

        self.assertEqual(signature,"nqxpgHpye%2BdOEkEbC%2FS3N1%2FCRFlZPHoyRztkRhkCoz7ISNmV9V60TQ7zwS8Q59SGQUGYuoNSVe8SWtNVQTEuRiZfXd6Eme%2BCdHfAt7%2BbNd3UsrcIHl3CJEvx7u70ItW8aOx4F7rjF%2BaIOq%2Bpc0rbuBugF%2BnElGKydpPiQrKKwE5kB3TZKVkYLLCsLU8Ry%2Fjg05d2TcnGTyfYZDchV4ui0uPzR5UH%2Fkb4ni8lchrtAeaGJwCimACIk6qNLoNnz7u9joKHtYeuZhORRVodxKB%2BAolgAQqJBMyLrseJDITmwIRTRSzQ3vclt%2BMvVs1CMbXYuvnDYd5NFv98emJgBC%2FX1A%3D%3D")




if __name__ == '__main__':
    unittest.main()
