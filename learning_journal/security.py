# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyramid.security import Allow, Everyone, Authenticated, ALL_PERMISSIONS
from passlib.apps import custom_app_context as pwd_context
import os
from wtforms.ext.csrf import SecureForm
from hashlib import md5


SECRET_KEY = 'this_is_secret'


def check_password(pw):
    """Check if provided password matches password hash."""
    hashed = os.environ.get('AUTH_PASSWORD', 'this is not a password')
    return pwd_context.verify(pw, hashed)


class DefaultRoot(object):
    """Base user authorization."""
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request

class SuperSecureForm(SecureForm):
    """Secure a form with CSRF protection."""

    def generate_csrf_token(self, csrf_context):
        """Generate a CSRF Token."""
        params = SECRET_KEY + crsf_context
        token = md5(params.encode('utf-8')).hexdigest()
        return token

    def validate_csrf_token(self, field):
        """Validate a CSRF token."""
        if field.data != field.current_token:
            raise ValueError('Invalid CSRF')
