from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class FlashcardForm(FlaskForm):
    front = StringField("Front", validators=[DataRequired()])
    back = StringField("Back", validators=[DataRequired()])
    submit = SubmitField("Add Flashcard")
