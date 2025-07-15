from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from problems.models import Problem, Tag
# Create your models here.

class CodeSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True, blank=True)
    language = models.CharField(max_length=100)
    code = models.TextField()
    input_data = models.TextField(null=True,blank=True)
    output_data = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    verdict = models.CharField(max_length=50, blank=True, null=True) # e.g., "Accepted", "Wrong Answer"
    score = models.FloatField(default=0.0)
    submitted_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return f"Submission by {self.user.username} for {self.problem.title} in {self.language}"