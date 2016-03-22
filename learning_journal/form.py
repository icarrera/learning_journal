from wtforms import Form, StringField, validators, TextAreaField


class JournalForm(Form):

    """Create a form for our learning journal entries."""
    title = StringField('title', [validators.Length(min=1, max=128)])
    text = TextAreaField('text')


class LoginForm(Form):

    """Create a login form for user authentication."""
    username = StringField('username', [validators.Length(min=1)])
    password = StringField('password', [validators.Length(min=5)])
