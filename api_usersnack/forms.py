from wtforms import Form, StringField, IntegerField, validators


class SubmitForm(Form):
    name = StringField('Name')
    address = StringField('Address', [validators.Length(min=6, max=50)])
    pizza = IntegerField('Pizza')