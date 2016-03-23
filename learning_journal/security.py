# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyramid.security import Allow, Everyone, Authenticated, ALL_PERMISSIONS
from passlib.apps import custom_app_context as pwd_context
import os

def check_password(pw):
    hashed = os.environ.get('AUTH_PASSWORD', 'this is not a password')
    return pwd_context.verify(pw, hashed)


class DefaultRoot(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request
