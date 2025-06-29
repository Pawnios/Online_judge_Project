from django import forms
from compiler.submit.models import code_submission

language_choices=[
    ("py","Python"),
    ("c","C"),
    ("cpp","C++"),
]

class code_submission_form(forms.ModelForm):
    language=forms.ChoiceField(choices=language_choices)

    class Meta:
        model=code_submission
        fields=["language","code","input_data"]