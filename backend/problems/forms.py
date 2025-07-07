from django import forms
from .models import Problem, Tag, TestCase  # Make sure to import your models

class ProblemForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'tag-selector',
            'multiple': 'multiple'
        }),
        required=False
    )
    
    class Meta:
        model = Problem  
        fields = '__all__'
        labels = {
    'title': 'Problem Name',
    'statement': 'Problem Statement',
    'difficulty': 'Difficulty Level',
    'TestCase': 'Test Cases',
    'tags': 'Problem Tags',  
}
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'eg. Two Sum'}),  # Changed from 'name' to 'title'
            'statement': forms.Textarea(attrs={'placeholder': 'eg. Given an array...'}),
            'difficulty': forms.Select(),
        }

# class ProblemForm(forms.ModelForm):
#     class Meta:
#         model = Problem
#         fields = '__all__'
#         labels = {
#             'title': 'Problem Name',
#             'statement': 'Problem Statement',
#             'difficulty': 'Difficulty Level',
#             'TestCase': 'Test Cases',
#         }
#         tags = forms.ModelMultipleChoiceField(
#         queryset=Tag.objects.all(),
#          widget=forms.SelectMultiple(attrs={
#             'class': 'tag-selector',
#             'multiple': 'multiple'
#         }),
#         required=False
#     )

#         widgets = {
#             'name': forms.TextInput(attrs={'placeholder': 'eg. Two Sum'}),
#             'statement': forms.Textarea(attrs={'placeholder': 'eg. Given an array...'}),
#             'difficulty': forms.Select(),
            
#         }

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['input_data', 'expected_output', 'is_hidden']
        labels = {
            'input_data': 'Input Data',
            'expected_output': 'Expected Output',
            'is_hidden': 'Is Hidden',
        }

        widgets = {
            'input_data': forms.Textarea(attrs={'placeholder': 'eg. 1 2 3'}),
            'expected_output': forms.Textarea(attrs={'placeholder': 'eg. 6'}),
            # 'order': forms.NumberInput(),
            'is_hidden': forms.CheckboxInput(),
        }           