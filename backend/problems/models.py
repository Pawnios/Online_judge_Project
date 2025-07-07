
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
    
class Problem(models.Model):
    p_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    statement = models.TextField()
    difficulty = models.CharField(max_length=50, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='problems',blank=True) 

    def __str__(self):
        return self.title
    

class TestCase(models.Model):
    input_data = models.TextField()
    expected_output = models.TextField()
    is_hidden = models.BooleanField(default=False)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='testcases')

    def __str__(self):
        return f"TestCase for {self.problem.title} - Input: {self.input_data[:30]}..."
