
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
class Problem(models.Model):
    p_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    statement = models.TextField()
    difficulty = models.CharField(max_length=50, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
    

class TestCase(models.Model):
    input_data = models.TextField()
    expected_output = models.TextField()
    is_hidden = models.BooleanField(default=False)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='testcases')

    def __str__(self):
        return f"TestCase for {self.problem.title} - Input: {self.input_data[:30]}..."
    

# class TestCase(models.Model):
#     problem = models.ForeignKey(Problem, on_delete=models.CASCADE,related_name='testcases',null=True,blank=True)
#     difficulty = models.CharField(max_length=10, choices=[("Easy", "Easy"), ("Med.", "Medium"), ("Hard", "Hard")],null=True,blank=True)
#     description=models.TextField(null=True,blank=True)
    

#     # --- Visible Test Case Files (for 'Run') ---
#     input_file = models.FileField(upload_to='testcases/inputs/', help_text="File with visible test cases, separated by '---'")
#     output_file = models.FileField(upload_to='testcases/outputs/', help_text="File with corresponding visible outputs")
    
#     # --- NEW: Hidden Test Case Files (for 'Submit') ---
#     hidden_input_file = models.FileField(upload_to='testcases/hidden_inputs/', blank=True, null=True, help_text="Optional: File with hidden test cases")
#     hidden_output_file = models.FileField(upload_to='testcases/hidden_outputs/', blank=True, null=True, help_text="Optional: Corresponding hidden outputs")

#     is_visible = models.BooleanField(default=True) # This can now represent the visibility of the sample cases

#     constraints=models.TextField(null=True,blank=True)
#     explanations=models.TextField(null=True,blank=True)