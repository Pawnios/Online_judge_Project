from django.shortcuts import render
from django.http import HttpResponse
from compiler.submit.forms import code_submission_form
from django.conf import settings
import os
import uuid
import subprocess
from pathlib import Path

# Create your views here.

def submit(request):
    
    if request.method=="POST":
        form=code_submission_form(request.POST) #form created on backend (recommended frontend method)
        if form.is_valid():
            submission=form.save()
            print(submission.language)
            print(submission.code)
            #from output_data in run_code function
            output=run_code(
                submission.language, submission.code, submission.input_data
            )
            submission.output_data=output
            submission.save()
            return render(request, "index.html", {"submission" :submission,
                                                  "form":form, })
    else:
        #user just landed on this page
        form=code_submission_form()
        
    return render(request,"index.html",context={
            "form":form,
            
        })


def run_code(language, code, input_data):
    project_path=Path(settings.BASE_DIR)
    directories=["codes","inputs","outputs"]
    
    #3 folders created
    for directory in directories:
        dir_path=project_path/directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True,exist_ok=True)
    
    #directory names
    codes_dir=project_path/"codes"
    inputs_dir=project_path/"inputs"
    output_dir=project_path/"outputs"

    unique_str=str(uuid.uuid4())
    #file names
    code_file_name=f"{unique_str}.{language}"
    input_file_name=f"{unique_str}.txt"
    output_file_name=f"{unique_str}.txt"
    
    #unique paths
    code_file_path=codes_dir/code_file_name
    input_file_path=inputs_dir/input_file_name
    output_file_path=output_dir/output_file_name

    with open(code_file_path,"w") as code_file:
        code_file.write(code)

    with open(input_file_path,"w") as input_file:
        input_file.write(input_data)

    with open(output_file_path,"w") as output_file:
        pass #creates an empty file


#for each language

    if language=="cpp":
        executable_path=codes_dir/unique_str
        compile_result=subprocess.run(
            ["clang++",str(code_file_path),"-o",str(executable_path)]
        ) #clang++ demo.cpp -o demo
        if compile_result.returncode==0:
            with open(input_file_path,"r") as input_file:
                with open(output_file_path,"w") as output_file:
                    subprocess.run(
                        [str(executable_path)],
                        stdin=input_file,
                        stdout=output_file,
                    )
    # elif compile_result.returncode==1:
    #         print("Compilation Error")

    elif language=="py":
        with open(input_file_path,"r") as input_file:
            with open(output_file_path,"w") as output_file:
                subprocess.run(
                    ["python3", str(code_file_path)],
                    stdin=input_file,
                    stdout=output_file,
                    ) #python3 demo.py
    elif language == "c":
        executable_path = codes_dir / unique_str
        compile_result = subprocess.run(
            ["gcc", str(code_file_path), "-o", str(executable_path)],
            capture_output=True
        )
        if compile_result.returncode == 0:
            with open(input_file_path, "r") as input_file:
                with open(output_file_path, "w") as output_file:
                    subprocess.run(
                        [str(executable_path)],
                        stdin=input_file,
                        stdout=output_file,
                    )
        else:
            return compile_result.stderr.decode()
        
    elif language == "java":
    # ALWAYS enforce class name Main
        class_name = "Main"
        java_code_file_path = codes_dir / f"{class_name}.java"
        with open(java_code_file_path, "w") as f:
            f.write(code)

    # Compile
        compile_result = subprocess.run(
            ["javac", str(java_code_file_path)],
            capture_output=True,
            cwd=codes_dir
            )
        if compile_result.returncode != 0:
            return compile_result.stderr.decode()

    # Run
        with open(input_file_path, "r") as infile, open(output_file_path, "w") as outfile:
            subprocess.run(
                ["java", "-cp", str(codes_dir), class_name],
                stdin=infile,
                stdout=outfile,
                stderr=subprocess.STDOUT
            )

    else:
        return f"Language '{language}' not supported."
#reading output
    with open(output_file_path,"r") as output_file:
        output_data=output_file.read()

    return output_data