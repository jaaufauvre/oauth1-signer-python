# oauth1-signer-python

[![](https://img.shields.io/badge/license-MIT-yellow.svg)](https://github.com/Mastercard/oauth1-signer-java/blob/master/LICENSE)

## Table of Contents
- [Overview](#overview)
  * [Compatibility](#compatibility)
  * [References](#references)
- [Usage](#usage)
  * [Prerequisites](#prerequisites)
  * [Adding the Library to Your Project](#adding-the-library-to-your-project)
  * [Loading the Signing Key](#loading-the-signing-key) 
  * [Creating the OAuth Authorization Header](#creating-the-oauth-authorization-header)

## Overview <a name="overview"></a>
Zero dependency library for generating a Mastercard API compliant OAuth signature.

### Compatibility <a name="compatibility"></a>
Python 3.7.x

### References <a name="references"></a>
* [OAuth 1.0a specification](https://tools.ietf.org/html/rfc5849)
* [Body hash extension for non application/x-www-form-urlencoded payloads](https://tools.ietf.org/id/draft-eaton-oauth-bodyhash-00.html)

## Usage <a name="usage"></a>
### Prerequisites <a name="prerequisites"></a>
Before using this library, you will need to set up a project in the [Mastercard Developers Portal](https://developer.mastercard.com). 

As part of this set up, you'll receive credentials for your app:
* A consumer key (displayed on the Mastercard Developer Portal)
* A private request signing key (matching the public certificate displayed on the Mastercard Developer Portal)

### Adding the Library to Your Project <a name="adding-the-library-to-your-project"></a>

#### PIP
`pip install git+https://github.com/Mastercard/oauth1-signer-python.git`

####or Clone 
`git clone https://github.com/Mastercard/oauth1-signer-python.git`

Change to the repo folder, and enter :

`python3 setup.py install`



### Loading the Signing Key <a name="loading-the-signing-key"></a>

A `PrivateKey` key object can be created by calling the `AuthenticationUtils.loadSigningKey` method:
```python
    keyfile = join(dirname(dirname(realpath(__file__))), "folder", "keyfile.p12")
    signing_key = authenticationutils.load_signing_key(keyfile, "password")
    consumer_key = OAuthSigner("uLXKmWNmIkzIGKfA2injnNQqpZaxaBSKxa3ixEVu2f283c95!33b9b2bd960147e387fa6f3f238f07170000000000000000", signing_key)

```

### Creating the OAuth Authorization Header <a name="creating-the-oauth-authorization-header"></a>
The method that does all the heavy lifting is `OAuth.getAuthorizationHeader`. You can call into it directly and as long as you provide the correct parameters, it will return a string that you can add into your request's `Authorization` header.

```python
        uri = "https://sandbox.api.mastercard.com/service"
        method = "POST"
        header = OAuth.get_authorization_header(self, uri, method, "payload", self.consumer_key, self.signing_key)
```

