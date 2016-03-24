# -*- coding: utf-8 -*-
from pyramid.testing import DummyRequest


def test_list_view(new_entry):
    """Test if the list view returns the expected title."""
    from learning_journal.views import list_view
    response = list_view(DummyRequest())
    assert response['entries'][0].title == "test post"


def test_detail_view_unit(new_entry):
    """Test if the detail view returns the expected title and text."""
    from learning_journal.views import detail_view
    this_id = str(new_entry.id)
    req = DummyRequest()
    req.matchdict = {'this_id': this_id}
    response = detail_view(req)
    assert response['entry'].title == 'test post'
    assert response['entry'].text == 'zomg testing'


def test_home_route_fxn(dbtransaction, app):
    """Test our home route functionality."""
    response = app.get('/')
    assert response.status_code == 200


def test_detail_view_fxn(new_entry, app):
    """Test detail route functionality."""
    response = app.get('/detail/{}'.format(new_entry.id))
    assert response.status_code == 200
    assert new_entry.title in response
