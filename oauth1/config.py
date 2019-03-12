#!/usr/bin/env python
# -*- coding: utf-8 -*- 
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

"""
Config File for MasterCard APIs Core SDK
"""


class Config(object):
    """
    Configurable options for MasterCard APIs Core SDK
    """

    debug = False
    authentication = None
    registered_instances = {}
    proxy = {}
    connection_timeout = 5
    read_timeout = 30

    def __init__(self):
        pass

    @classmethod
    def set_debug(cls, debug):
        cls.debug = debug

    @classmethod
    def is_debug(cls):
        return cls.debug

    @classmethod
    def set_proxy(cls, proxy):
        cls.proxy = proxy

    @classmethod
    def get_proxy(cls):
        return cls.proxy

    @classmethod
    def get_read_timeout(cls):
        return cls.read_timeout

    @classmethod
    def set_read_timeout(cls, timeout):
        if timeout:
            cls.read_timeout = timeout
        else:
            cls.read_timeout = 30

    @classmethod
    def get_connection_timeout(cls):
        return cls.connection_timeout

    @classmethod
    def set_connection_timeout(cls, timeout):
        if timeout:
            cls.connection_timeout = timeout
        else:
            cls.connection_timeout = 5

    @classmethod
    def set_authentication(cls, authentication):
        cls.authentication = authentication

    @classmethod
    def get_authentication(cls):
        return cls.authentication

    @classmethod
    def set_environment(cls, environment):
        if environment:
            cls.environment = environment
            for registered_instance in list(cls.registered_instances.values()):
                registered_instance.set_environment(environment)

    @classmethod
    def register_resource_config(cls, resource_config):
        class_name = resource_config.getName()
        if class_name not in list(cls.registered_instances.keys()):
            cls.registered_instances[class_name] = resource_config

    @classmethod
    def clear_resource_config(cls):
        cls.registered_instances = {}
