import hackbright_app
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/project")
def project():
    return render_template("project.html")

@app.route("/get_project")
def get_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project")
    project_grades = hackbright_app.grades_for_projects(project_title)
    html = render_template("project_info.html", students=project_grades,
                                                project_name=project_title)
    return html

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("student")
    student_data = hackbright_app.get_student_by_github(student_github)
    student_grades = hackbright_app.show_all_student_grades(student_data[0], student_data[1])
    html = render_template("student_info.html", first_name=student_data[0],
                                                last_name=student_data[1],
                                                github=student_data[2],
                                                grades=student_grades)


    return html

@app.route("/new_student")
def new_student():
    return render_template("new_student.html")

@app.route("/new_student_created")
def new_student_created():
    hackbright_app.connect_to_db()
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    github = request.args.get("github")
    status = hackbright_app.make_new_student(first_name, last_name, github)
    if status == 1:    
        return render_template("new_student_created.html",
                                  first_name=first_name,
                                  last_name=last_name,
                                  github=github)    
    else:
        return render_template("error.html", error_message="Oops, we failed to create the new student %s %s."%(first_name,last_name))

@app.route("/new_project")
def new_project():
    return render_template("new_project.html")


@app.route("/new_project_created")
def new_project_created():
    hackbright_app.connect_to_db()
    title = request.args.get("title")
    description = request.args.get("description")
    max_grade = request.args.get("max_grade")
    status = hackbright_app.add_a_project(title, description, max_grade)

    if status == 1:    
        return render_template("new_project_created.html",
                                  title=title,
                                  description=description,
                                  max_grade=max_grade)    
    else:
        return render_template("error.html", error_message="Oops, we failed to create the new project %s."%(title))

@app.route("/give_grade")
def give_grade():
    return render_template("give_grade.html")

@app.route("/grade_given")
def grade_given():
    hackbright_app.connect_to_db()
    github = request.args.get("github")
    project = request.args.get("project")
    grade = request.args.get("grade")
    status = hackbright_app.give_student_grade(github, project, grade)

    if status == 1:    
        return render_template("grade_given.html",
                                  github=github,
                                  project=project,
                                  grade=grade)    
    else:
        return render_template("error.html", error_message="Oops, we failed to add the grade %s to the project %s for account %s."%(grade, project, github))    
    
@app.route("/")
def get_github():
    return render_template("get_github.html")

if __name__ == "__main__":
    app.run(debug=True)