# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyramid.security import Allow, Everyone
from pyramid.security import ALL_PERMISSIONS
from .models import Entry

def DefaultRoot(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'g:users', ALL_PERMISSIONS)
    ]

    def __init__(self, request):
        self.request = request


def userfinder(userid, request):
    """Return none if userid is inaccurate."""
    groups = []
    if userid.lower() in request.users:
        groups.append('g:users')
    return groups or None

class EntryRoot(object):

    __name__ = 'entry'

    @property
    def __parent__(self):
        return DefaultRoot(self.request)

    def __init__(self, request):
        self.request = request

    def __getitem__(self, name):
        entry_obj = Entry.by_id(name)
        if entry_obj is None:
            raise KeyError(name)
        entry_obj.__parent__ = self
        return entry_obj
