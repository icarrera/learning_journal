# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyramid.security import Allow, Everyone, ALL_PERMISSIONS


def DefaultRoot(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'iris', ALL_PERMISSIONS)
    ]

    def __init__(self, request):
        self.request = request
