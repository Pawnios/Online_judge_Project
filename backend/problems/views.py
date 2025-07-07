
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ProblemForm, TestCaseForm
from .models import Problem, TestCase
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required as admin_required

from django.contrib.auth.decorators import login_required

# Create your views here.
@admin_required
def add_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save()
            messages.success(request, 'Problem added successfully!')
            return redirect('problems')
    else:
        form = ProblemForm()
    return render(request, 'add_problem.html', {'form': form})



@admin_required
def updateView(request, f_oid):
    obj = Problem.objects.get(oid=f_oid)
    form = ProblemForm(instance=obj)
    if request.method == 'POST':
        form = ProblemForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('problems')
    template_name = 'problem_list.html'
    context = {'form': form}
    return render(request, template_name, context)

@admin_required
def add_test_case(request, problem_id):
    try:
        problem = Problem.objects.get(pk=problem_id)
        if request.method == 'POST':
            test_case = TestCase(
                problem=problem,
                input_data=request.POST.get('input'),
                expected_output=request.POST.get('output')
            )
            test_case.save()
            return redirect('problem_detail', problem_id=problem.id)
    except Problem.DoesNotExist:
        raise Http404("Problem does not exist")


def problem_list(request):
    problems = Problem.objects.all().prefetch_related('tags')
    return render(request, 'problem_list.html', {'problems': problems})

@login_required
def problem_detail(request, p_id):
    problem = get_object_or_404(Problem, p_id=p_id)
    test_cases = problem.testcases.filter(is_hidden=False)
    return render(request, 'problems/problem_detail.html', {
        'problem': problem,
        'test_cases': test_cases
    })