# from django.shortcuts import render, get_object_or_404
# from .models import Problem

# def problem_list(request):
#     problems = Problem.objects.all().order_by('-created_at')
#     return render(request, 'problem_list.html', {'problems': problems})

# def problem_detail(request, pk):
#     problem = get_object_or_404(Problem, pk=pk)
#     return render(request, 'problem_detail.html', {'problem': problem, 'testcases': problem.testcases.all(), 'pk': pk, 'title': problem.title, 'description': problem.description, 'difficulty': problem.difficulty, 'created_at': problem.created_at, 'updated_at': problem.updated_at, })
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ProblemForm, TestCaseForm
from .models import Problem, TestCase
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required as admin_required

# Create your views here.
@admin_required
def add_problem(request):
    form = ProblemForm()
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/problems')
    template_name = 'add_problem.html'
    context = {'form': form}
    return render(request, template_name, context)


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
def addTestCaseView(request, f_oid):
    obj = Problem.objects.get(oid=f_oid)
    form = TestCaseForm()
    if request.method == 'POST':
        form = TestCaseForm(request.POST)
        if form.is_valid():
            test_case = form.save(commit=False)
            test_case.problem = obj
            test_case.save()
            messages.success(request, 'Test case added successfully!')
            return redirect('problems')
    template_name = 'problem_list.html'
    context = {'form': form, 'obj': obj}
    return render(request, template_name, context)

@admin_required
def deleteView(request, f_oid):
    obj = Problem.objects.get(oid=f_oid)
    if request.method == 'POST':
        obj.delete()
        return redirect('problems')
    template_name = 'problem_list.html'
    context = {'obj': obj}
    return render(request, template_name, context)

def problem_list(request):
    problems = Problem.objects.all().prefetch_related('tags')
    return render(request, 'problem_list.html', {'problems': problems})

@login_required
def show_problem(request, p_id):
    problem = get_object_or_404(Problem, p_id=p_id)
    return render(request, 'problem_detail.html', {'problem': problem, 'testcases': problem.testcases.all(), 'p_id': p_id, 'title': problem.title, 'statement': problem.statement, 'difficulty': problem.difficulty, 'created_at': problem.created_at, 'updated_at': problem.updated_at, 'is_hidden': problem.testcases.filter(is_hidden=True).exists()})