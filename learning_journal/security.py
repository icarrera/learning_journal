# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyramid.security import Allow, Everyone, ALL_PERMISSIONS
#

class DefaultRoot(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'iris', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request

#
# import os
# # class example
#
# from passlib.apps import custom_apps_context as pwd_context
#
# def check_pw(pw):
#     hashed = os.environ.get('AUTH_PASSWORD', 'this is not a password')
#     return pwd_context.verify(pw, hashed)
