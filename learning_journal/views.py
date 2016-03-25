from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from .form import JournalForm, LoginForm
from sqlalchemy import desc
import markdown
from .security import check_password

from .models import (
    DBSession,
    Entry,
    )


@view_config(route_name='login', renderer='templates/login_view.jinja2')
def login_view(request):
    """Login the user."""
    context = get_auth_tkt(request)
    form = LoginForm(request.POST, csrf_context=context)
    if request.method == 'POST' and form.validate():
        username = request.params.get('username', '')
        password = request.params.get('password', '')
        if check_password(password):
            headers = remember(request, username)
            return HTTPFound(location='/', headers=headers)
        else:
            message = 'login failed'
    else:
        message = 'please login'
    return {'message': message, 'form': form}


@view_config(route_name='logout', renderer='string')
def logout_view(request):
    """Logout the user."""
    headers = forget(request)
    return HTTPFound(location='/', headers=headers)


@view_config(route_name='home', renderer='templates/list_view.jinja2')
def list_view(request):
    """Handle the view of our home page."""
    return {'entries': DBSession.query(Entry).order_by(desc(Entry.created)).all()}


@view_config(route_name='detail_view', renderer='templates/detail_view.jinja2')
def detail_view(request):
    """Handle the view of a single journaly entry."""
    md = markdown.Markdown(safe_mode='replace', html_replacement_text='NO')
    this_id = request.matchdict['this_id']
    entry = DBSession.query(Entry).get(this_id)
    text = md.convert(entry.text)
    return {'entry': entry, 'text': text}


@view_config(route_name='add_view', renderer='templates/add_view.jinja2', permission='add')
def add_view(request):
    """Handle the view of our adding new entry page."""
    context = get_auth_tkt(request)
    form = JournalForm(request.POST, csrf_context=context)
    if request.method == "POST" and form.validate():
        new_entry = Entry(title=form.title.data, text=form.text.data)
        DBSession.add(new_entry)
        DBSession.flush()
        this_id = new_entry.id
        return HTTPFound(location='/detail/{}'.format(this_id))
    return {'form': form}


@view_config(route_name='edit_view', renderer='templates/add_view.jinja2', permission='edit')
def edit_view(request):
    """Handle the view of our edit entry page."""
    this_id = request.matchdict['this_id']
    entry = DBSession.query(Entry).get(this_id)
    context = get_auth_tkt(request)
    form = JournalForm(request.POST, entry, csrf_context=context)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        this_id = entry.id
        return HTTPFound(location='/detail/{}'.format(this_id))
    return {'form': form}


def get_auth_tkt(request):
    """Get an auth_tkt from a request for use with CSRF protection."""
    request_cookies = request.headers.items()
    auth_tkts = [value for cookie, value in request_cookies
                 if cookie == 'Cookie' and value.startswith('auth_tkt')]
    if not auth_tkts:
        return ''
    return auth_tkts[0]
