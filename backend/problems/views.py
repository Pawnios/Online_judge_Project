
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ProblemForm, TestCaseForm
from .models import Problem, TestCase, Tag
from django.http import HttpResponse, Http404, JsonResponse
import json
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required as admin_required
import google.generativeai as genai
import logging
import backend.settings
from submission.models import CodeSubmission
import subprocess
from pathlib import Path
from django.conf import settings
import uuid
import os
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
from django.db.models import OuterRef, Exists
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
# Create your views here.
@admin_required
def add_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save()
            
            # Process test cases
            test_cases_json = request.POST.get('test_cases', '[]')
            try:
                test_cases = json.loads(test_cases_json)
                for test_case in test_cases:
                    TestCase.objects.create(
                        problem=problem,
                        input_data=test_case['input'],
                        expected_output=test_case['output']
                    )
                messages.success(request, 'Problem and test cases added successfully!')
                return redirect('/problems')
            except json.JSONDecodeError:
                messages.error(request, 'Invalid test cases data')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = ProblemForm()
    
    return render(request, 'problems/add_problem.html', {'form': form})


from django.db.models import Exists, OuterRef, Q
from django.contrib.auth.decorators import login_required

@login_required
def problem_list(request):
    problems = Problem.objects.annotate(
        is_solved=Exists(
            CodeSubmission.objects.filter(
                Q(problem=OuterRef('p_id')),
                Q(user=request.user),
                Q(verdict='AC') | Q(score=100)  # Either accepted or 100% score
            )
        )
    ).order_by('p_id')
    
    return render(request, 'problems/problem_list.html', {
        'problems': problems
    })


@login_required
def problem_detail(request, p_id):
    problem = get_object_or_404(Problem, p_id=p_id)
    test_cases = problem.testcases.filter(is_hidden=False)
    
    return render(request, 'problems/problem_detail.html', {
        'problem': problem,
        'test_cases': test_cases
    })


genai.configure(api_key=backend.settings.GEMINI_API_KEY)
model= genai.GenerativeModel('models/gemini-2.0-flash')

 