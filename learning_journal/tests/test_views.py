# -*- coding: utf-8 -*-
from pyramid.testing import DummyRequest
from learning_journal.models import Entry, DBSession
import pytest
from learning_journal.views import (
    list_view,
    detail_view,
    add_view,
    edit_view
    )
