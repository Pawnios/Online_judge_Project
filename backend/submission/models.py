from django.db import models
from django.contrib.auth.models import User
from problems.models import Problem, Tag

class CodeSubmission(models.Model):
    VERDICT_CHOICES = [
        ('AC', 'Accepted'),
        ('WA', 'Wrong Answer'),
        ('TLE', 'Time Limit Exceeded'),
        ('CE', 'Compilation Error'),
        ('RE', 'Runtime Error'),
    ]
    
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('c', 'C'),
    ]
  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    code = models.TextField()
    input_data = models.TextField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)
    verdict = models.CharField(max_length=3, choices=VERDICT_CHOICES)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f" {self.user.username}'s submission for {self.problem.title}"