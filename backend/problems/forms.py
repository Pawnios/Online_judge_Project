from django import forms
from .models import Problem as problems, TestCase 

class ProblemForm(forms.ModelForm):
    class Meta:
        model = problems
        fields = '__all__'
        labels = {
            'name': 'Problem Name',
            'statement': 'Problem Statement',
            'difficulty': 'Difficulty Level',
            'TestCase': 'Test Cases',
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'eg. Two Sum'}),
            'statement': forms.Textarea(attrs={'placeholder': 'eg. Given an array...'}),
            'difficulty': forms.Select(),
        }

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