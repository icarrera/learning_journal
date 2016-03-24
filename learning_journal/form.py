from wtforms import StringField, validators, TextAreaField
from .security import SuperSecureForm


class JournalForm(SuperSecureForm):
    """Create a form for our learning journal entries."""

    title = StringField('title', [validators.Length(min=1, max=128)])
    text = TextAreaField('text')


class LoginForm(SuperSecureForm):
    """Create a login form for user authentication."""

    username = StringField('username', [validators.Length(min=1)])
    password = StringField('password', [validators.Length(min=5)])
