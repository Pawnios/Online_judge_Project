
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
from executor.models import CodeSubmission
import subprocess
from pathlib import Path
from django.conf import settings
import uuid
import os
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
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


def problem_list(request):
    problems = Problem.objects.all().prefetch_related('tags')
    all_tags = Tag.objects.all().order_by('name')
    # # Get set of problem IDs solved by this user
    # solved_problems = set(
    #     UserSolvedProblem.objects.filter(user=User).values_list('problem_id', flat=True)
    # )

    # # Add is_solved attribute to each problem
    # for problem in problems:
    #     problem.is_solved = problem.id in solved_problems
    return render(request, 'problems/problem_list.html', {'problems': problems})

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

    
def run_code(language, code, input_data):
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    # Make sure the necessary directories exist
    for directory in directories:
        dir_path = project_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())

    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    # Save the code to file
    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    # Normalize input line endings
    input_data = (input_data or "").replace("\r\n", "\n")

    with open(input_file_path, "w") as input_file:
        input_file.write(input_data)

    with open(output_file_path, "w") as output_file:
        pass  # Create an empty output file

    output_data = ""
    error_data = ""

    try:
        if language == "cpp":
            executable_path = codes_dir / unique

            if not code_file_name.endswith('.cpp'):
                code_file_name = f"{unique}.cpp"
                code_file_path = codes_dir / code_file_name
            # Compile
            compile_result = subprocess.run(
                ["g++", str(code_file_path), "-o", str(executable_path)],
                capture_output=True, text=True, timeout=5
            )
            if compile_result.returncode != 0:
                error_data = compile_result.stderr
            else:
                # Run the program
                run_result = subprocess.run(
                    [str(executable_path)],
                    stdin=open(input_file_path, "r"),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5
                )
                output_data = run_result.stdout
                error_data = run_result.stderr

        elif language == "py":
            run_result = subprocess.run(
                ["python", str(code_file_path)],
                stdin=open(input_file_path, "r"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
            output_data = run_result.stdout
            error_data = run_result.stderr

    except subprocess.TimeoutExpired:
        error_data = "Error: Timeout - Your code took too long to execute."
    except Exception as e:
        error_data = f"Error: {str(e)}"

    # Clean up files
    try:
        os.remove(code_file_path)
        os.remove(input_file_path)
        if language == "cpp" and 'executable_path' in locals():
            os.remove(executable_path)
    except:
        pass

    # Combine output and error
    final_output = output_data.strip()
    if error_data:
        final_output += "\n\nErrors:\n" + error_data.strip()

    return final_output


def run_testcases(submission, problem, visible_only=False):
    # Get all test cases for the problem
    test_cases = TestCase.objects.filter(problem=problem)
    
    if not test_cases.exists():
        return {'results': [], 'total_testcases': 0, 'passed_testcases': 0, 'score': 0}

    all_results = []
    total_testcases = 0
    passed_testcases = 0

    try:
        # Filter test cases based on visibility
        if visible_only:
            test_cases = test_cases.filter(is_hidden=False)
        
        total_testcases = test_cases.count()

        for case in test_cases:
            output = run_code(submission.language, submission.code, case.input_data).strip()
            passed = output.replace('\r\n', '\n') == case.expected_output.replace('\r\n', '\n')

            if passed:
                passed_testcases += 1
            
            all_results.append({
                'input': case.input_data, 
                'expected': case.expected_output,
                'output': output, 
                'passed': passed, 
                'visible': not case.is_hidden
            })

    except Exception as e:
        all_results.append({
            'input': "Error processing test cases", 
            'expected': "N/A",
            'output': f"System Error: {str(e)}", 
            'passed': False, 
            'visible': True
        })
        total_testcases = 1

    return {
        'results': all_results,
        'total_testcases': total_testcases,
        'passed_testcases': passed_testcases,
        'score': (passed_testcases / total_testcases * 100) if total_testcases > 0 else 0
    }


@login_required
def submit(request, p_id):
    print("--- SUBMIT VIEW CALLED ---")
    problem = get_object_or_404(Problem, p_id=p_id)
    test_cases = TestCase.objects.filter(problem=problem, is_hidden=False)

    # Prepare context with visible test cases
    context = {
        "problem": problem,
        "test_cases": test_cases,
    }

    if request.method == "POST":
        language = request.POST.get("language")
        code = request.POST.get("code")
        input_data = request.POST.get("input_data", "")
        action = request.POST.get("action")
        
        submission = CodeSubmission(language=language, code=code, input_data=input_data)
        context["submission"] = submission

        # --- ACTION: AI HELP ---
        if action == "ai_help":
            if not code.strip():
                messages.error(request, "Code is empty. Please write a solution before seeking AI help.")
                return redirect('submit_question', p_id=p_id)
            return ai_help(request, problem)

        # --- ACTION: RUN CODE ---
        elif action == "run":
            if input_data.strip():
                output = run_code(submission.language, submission.code, input_data)
                context["custom_run_result"] = {
                    'input': input_data,
                    'output': output
                }
            else:
                if not code.strip():
                    messages.error(request, "Code is empty. Please write a solution before running.")
                    return redirect('submit_question', p_id=p_id)
                else:
                    context["test_results"] = run_testcases(submission, problem, visible_only=True)

        # --- ACTION: SUBMIT CODE ---
        elif action == "submit":
            if not code.strip():
                messages.error(request, "Code is empty. Please write a solution before submitting.")
                return redirect('submit_question', p_id=p_id)
            
            test_results = run_testcases(submission, problem, visible_only=False)
            context["test_results"] = test_results
            
            # Save submission results
            final_verdict = "Accepted" if test_results.get('score') == 100 else "Wrong Answer"
            CodeSubmission.objects.create(
                user=request.user,
                problem=problem,
                language=language,
                code=code,
                score=test_results.get('score', 0),
                verdict=final_verdict
            )
        
        return render(request, "problem_detail.html", context)

    return render(request, "problem_detail.html", context)


def ai_help(request, problem):
    """
    Handles the AI help request using a structured, dynamic prompt.
    """
    language = request.POST.get("language")
    code = request.POST.get("code")
    input_data = request.POST.get("input_data", "")
    submission = CodeSubmission(language=language, code=code, input_data=input_data)
    test_results = run_testcases(submission, problem, visible_only=False)
    failed_tests = [res for res in test_results['results'] if not res['passed']]

    # Build the prompt
    prompt_context = [
        f"You are an expert AI code reviewer for an online programming judge. Your primary goal is to provide concise, structured, and helpful feedback on a user's code submission in about 200 words.",
        f"\n**Context:**",
        f"- **Problem:** {problem.statement}",
        f"- **Language:** {language}",
        f"- **User's Code:**\n``````"
    ]

    if not failed_tests:
        prompt_context.append("- **Test Results:** All test cases passed successfully.")
        prompt_context.append("\n**Your Task:**\nGenerate a response focusing *only* on the 'Code Review & Suggestions' section. Omit the 'Debugging Analysis' section entirely.")
    else:
        failed_details = ["- **Test Results:** The code failed the following test cases:"]
        for test in failed_tests:
            failed_details.append(
                f"  - **Input:** `{test['input']}`\n"
                f"    **Expected Output:** `{test['expected']}`\n"
                f"    **Actual Output:** `{test['output']}`"
            )
        prompt_context.append("\n".join(failed_details))
        prompt_context.append("\n**Your Task:**\nGenerate a response with both the 'Code Review & Suggestions' and 'Debugging Analysis' sections.")

    prompt_context.append(
        "\n---\n\n"
        "**1. Code Review & Suggestions**\n"
        "*   **Style Analysis:**\n"
        "*   **Improvements:**\n\n"
        "**2. Debugging Analysis**\n"
        "*   **[This section should only be included if test cases have failed]**\n"
        "*   **Bug:**\n"
        "*   **Explanation:**\n"
        "*   **Corrected Code:**"
    )

    prompt = "\n".join(prompt_context)

    try:
        my_api_key = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=my_api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=400
        )

        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        ai_response_text = response.text
    except Exception as e:
        ai_response_text = f"Could not get AI response. Error: {e}"

    # Get visible test cases for display
    test_cases = TestCase.objects.filter(problem=problem, is_hidden=False)
    
    return render(request, "problem_detail.html", {
        "problem": problem,
        "test_cases": test_cases,
        "submission": submission,
        "test_results": test_results,
        "ai_response": ai_response_text,
    })


@login_required
def submission_history_view(request, p_id):
    problem = get_object_or_404(Problem, p_id=p_id)
    
    submissions = CodeSubmission.objects.filter(
        user=request.user, 
        problem=problem
    ).order_by('-submitted_at')

    context = {
        'problem': problem,
        'submissions': submissions,
    }
    return render(request, 'submission_history.html', context)