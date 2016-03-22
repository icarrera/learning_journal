# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyramid.security import Allow, Everyone
from pyramid.security import ALL_PERMISSIONS
from .models import Entry

def DefaultRoot(object):
    """ACL DefaultRoot object."""
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'g:admins', ALL_PERMISSIONS)
    ]

    def __init__(self, request):
        self.request = request

def userfinder(userid, request):
    groups = []
    if userid.lower() in request.admins:
        groups.append('g:admins')
    return groups or None
