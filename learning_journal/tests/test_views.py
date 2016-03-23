# -*- coding: utf-8 -*-
# from pyramid.testing import DummyRequest
# from learning_journal.models import Entry, DBSession
# import webtest
# import pytest
# from learning_journal.views import (
#     list_view,
#     detail_view,
#     add_view,
#     edit_view
#     )


# def test_add_view_text(dbtransaction):
#     """Test for entry view dictionary text attribute."""
#     new_model = Entry(title="test 1", text='test text')
#     DBSession.add(new_model)
#     DBSession.flush()
#     test_request = DummyRequest()
#     test_request.matchdict = {'id': new_model.id}
#     dic = add_view(test_request)
#     assert dic['entry'].text == 'text text'
#
#
#
# def test_home_route(dbtransaction, app):
#     """Test our home route."""
#     response = app.get('/')
#     assert response.status_code == 200
