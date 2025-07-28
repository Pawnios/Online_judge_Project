from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from problems.models import Problem, TestCase
from .models import CodeSubmission
import subprocess
import os
from django.conf import settings
import uuid
from pathlib import Path
import google.generativeai as genai
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

@login_required
def run_code(request, p_id):
    problem = get_object_or_404(Problem, p_id=p_id)
    
    if request.method == 'POST':
        language = request.POST.get('language')
        code = request.POST.get('code', '').strip()  # Get and strip whitespace
        input_data = request.POST.get('input_data', '')
        
        
        
        # Save the submission
        submission = CodeSubmission.objects.create(
            user=request.user,
            problem=problem,
            language=language,
            code=code,
            input_data=input_data,
            verdict='PD'  # Pending
        )
        
        try:
            # Run the code
            output = execute_code(language, code, input_data)
            
            # Update submission with output
            submission.output = output
            submission.save()
            
            return render(request, 'submission/result.html', {
                'problem': problem,
                'submission': submission,
                'output': output
            })
            
        except Exception as e:
            logger.error(f"Code execution error: {str(e)}")
            messages.error(request, f"Error executing code: {str(e)}")
            return redirect('problems:problem_detail', p_id=p_id)
            
    return redirect('problems:problem_detail', p_id=p_id)


@login_required
def submit_code(request, p_id):
    problem = get_object_or_404(Problem, p_id=p_id)
    
    if request.method == 'POST':
        language = request.POST.get('language')
        code = request.POST.get('code')
        
        # Save the submission
        submission = CodeSubmission.objects.create(
            user=request.user,
            problem=problem,
            language=language,
            code=code,
            verdict='PD'  # Pending
        )
        
        # Run against test cases
        test_cases = TestCase.objects.filter(problem=problem)
        passed = 0
        total = test_cases.count()
        
        results = []
        for test_case in test_cases:
            output = execute_code(language, code, test_case.input_data)
            is_correct = output.strip() == test_case.expected_output.strip()
            
            if is_correct:
                passed += 1
                
            results.append({
                'input': test_case.input_data,
                'expected': test_case.expected_output,
                'output': output,
                'passed': is_correct,
                'visible': not test_case.is_hidden
            })
        
        # Calculate score and verdict
        score = int((passed / total) * 100) if total > 0 else 0
        verdict = 'AC' if score == 100 else 'WA'
        
        # Update submission
        submission.score = score
        submission.verdict = verdict
        submission.save()
        
        return render(request, 'submission/result.html', {
            'problem': problem,
            'submission': submission,
            'results': results,
            'passed': passed,
            'total': total,
            'score': score
        })

    return redirect('problems:problem_detail', p_id=p_id)

def detail(request, submission_id):
    """
    View to show details of a specific code submission
    """
    submission = get_object_or_404(CodeSubmission, id=submission_id)
    problem = submission.problem  # Get the problem from the submission
    
    return render(request, 'submission/detail.html', {
        'submission': submission,
        'code': submission.code,
        'problem': problem
    })

@login_required
def submission_history(request, p_id):
    problem = get_object_or_404(Problem, p_id=p_id)
    submissions = CodeSubmission.objects.filter(
        user=request.user,
        problem=problem
    ).order_by('-created_at')
    
    return render(request, 'submission/history.html', {
        'problem': problem,
        'submissions': submissions
    })

def execute_code(language, code, input_data):
    # Create unique directory for this execution
    unique_id = str(uuid.uuid4())
    exec_dir = Path(settings.BASE_DIR) / 'tmp' / unique_id
    exec_dir.mkdir(parents=True, exist_ok=True)
    
    # Prepare files
    code_file = exec_dir / f"code.{language}"
    input_file = exec_dir / "input.txt"
    output_file = exec_dir / "output.txt"
    
    # Write files
    with open(code_file, 'w') as f:
        f.write(code)
    
    with open(input_file, 'w') as f:
        f.write(input_data)
    
    # Execute based on language
    try:
        if language == 'python':
            result = subprocess.run(
                ['python', str(code_file)],
                stdin=open(input_file, 'r'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
        elif language == 'cpp':
            executable = exec_dir / "a.out"
            subprocess.run(
                ['g++', str(code_file), '-o', str(executable)],
                check=True,
                stderr=subprocess.PIPE,
                timeout=5
            )
            result = subprocess.run(
                [str(executable)],
                stdin=open(input_file, 'r'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
        # Add other languages as needed
        
        output = result.stdout
        if result.stderr:
            output += f"\n\nError:\n{result.stderr}"
            
    except subprocess.TimeoutExpired:
        output = "Error: Time Limit Exceeded"
    except subprocess.CalledProcessError as e:
        output = f"Error: {e.stderr}"
    except Exception as e:
        output = f"Error: {str(e)}"
    finally:
        # Clean up
        try:
            os.remove(code_file)
            os.remove(input_file)
            if language == 'cpp' and 'executable' in locals():
                os.remove(executable)
        except:
            pass
    
    return output




@login_required
def ai_helper(request, p_id):
    problem = get_object_or_404(Problem, p_id=p_id)
   

    if request.method == 'POST':
        language = request.POST.get('language', '').strip()
        code = request.POST.get('code', '').strip()
        
        # Validate input
        if not code:
            messages.error(request, "Code cannot be empty")
            return redirect('problems:problem_detail', p_id=p_id)
        if not language:
            messages.error(request, "Please select a programming language")
            return redirect('problems:problem_detail', p_id=p_id)

        try:
            # Configure Gemini AI
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            model = genai.GenerativeModel('models/gemini-2.0-flash')
            
            # Structured prompt for better AI response
            prompt = f"""
            **Code Review Request**
            
            **Problem Details:**
            - Title: {problem.title}
            - Difficulty: {problem.difficulty}
            - Description: {problem.statement}
            
            **Submission Details:**
            - Language: {language}
            - Code:
            ```{language.lower()}
            {code}
            ```
            
            **Please provide:**
            1. Code Quality Analysis (readability, style conventions)
            2. Correctness Check (potential bugs, edge cases)
            3. Optimization Suggestions (time/space complexity improvements)
            4. **Alternative Approaches** (different algorithms or paradigms)
            5. **Final Verdict** (overall assessment)
            
            Format your response with clear section headings.
            """
            
            # Generate response with safety settings
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 2000
                },
                safety_settings={
                    'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
                    'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                    'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                    'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE'
                }
            )
            
            # Process the response
            feedback = response.text
            if not feedback:
                raise ValueError("AI response is empty. Please try again.")
            
            return render(request, 'submission/ai_feedback.html', {
                'problem': problem,
                'feedback': feedback,
                'code': code,
                'language': language,
                'p_id': p_id
            })
            
        except Exception as e:
            logger.error(f"AI Helper Error: {str(e)}", exc_info=True)
            messages.error(request, f"AI service error: {str(e)}")
            return render(request, 'submission/ai_feedback.html', {
                'problem': problem,
                'error': str(e),
                'code': code,
                'language': language
            })

    # If not POST request, redirect to problem
    return redirect('submission/ai_feedback.html', p_id=p_id)




