
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ProblemForm, TestCaseForm
from .models import Problem, TestCase
from django.http import HttpResponse, Http404, JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required as admin_required
import google.generativeai as genai
import logging
import backend.settings
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


def problem_list(request):
    problems = Problem.objects.all().prefetch_related('tags')
    return render(request, 'problems/problem_list.html', {'problems': problems})

@login_required
def problem_detail(request, p_id):
    problem = get_object_or_404(Problem, p_id=p_id)
    test_cases = problem.testcases.filter(is_hidden=False)
    return render(request, 'problems/problem_detail.html', {
        'problem': problem,
        'test_cases': test_cases
    })



def ai_assist(request, p_id):
   problem = get_object_or_404(Problem, p_id=p_id)
   try:
        # Initialize Gemini API
        genai.configure(api_key=backend.settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        # Get user input
        user_code = request.POST.get('user_code', '').strip()
        user_question = request.POST.get('user_question', '').strip()
        
        if not user_question:
            return JsonResponse({'error': 'Please enter a question'}, status=400)
        
        # Create a structured prompt
        prompt = f"""
        You are a coding assistant helping with problem: {problem.title} (Difficulty: {problem.difficulty})
        
        Problem Statement:
        {problem.statement}
        
        User's Current Code:
        {user_code if user_code else 'No code provided'}
        
        User's Question:
        {user_question}
        
        Please provide:
        1. A concise explanation
        2. Suggestions for improvement (if code provided)
        3. Related concepts to consider
        4. Avoid giving complete solutions
        """
        
        # Get AI response
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 1000
            }
        )
        
        return JsonResponse({
            'response': response.text,
            'problem_id': p_id,
            'status': 'success'
        })
        
   except Exception as e:
        logger.error(f"AI Assist Error: {str(e)}")
        return JsonResponse({
            'error': 'Failed to get AI response. Please try again.',
            'status': 'error'
        }, status=500)
        