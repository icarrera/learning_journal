from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from learning_journal.security import DefaultRoot
import os

from .models import (
    DBSession,
    Base,
    )


def make_session(settings):
    from sqlalchemy.orm import sessionmaker
    engine = engine_from_config(settings, 'sqlalchemy')
    Session = sessionmaker(bind=engine)
    return Session()


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    if 'DATABASE_URL' in os.environ:
        settings['sqlalchemy.url'] = os.environ['DATABASE_URL']
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    secret = os.environ.get('AUTH_SECRET', 'secretstuff')
    authentication_policy = AuthTktAuthenticationPolicy(secret, hashalg='sha512')
    authorization_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        root_factory=DefaultRoot,
        authentication_policy=authentication_policy,
        authorization_policy=authorization_policy
    )

    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('detail_view', '/detail/{this_id}')
    config.add_route('add_view', '/add')
    config.add_route('edit_view', '/edit/{this_id}')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
