from flask import Flask, request, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)

app.debug = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = "bethechange"
toolbar = DebugToolbarExtension(app)


responses = []


@app.route("/")
def start():
    """Survey start page"""

    return render_template("start.jinja-html")


@app.route("/questions", methods=["GET", "POST"])
def root_redirect():
    """Redirect requsets to questions root (questions/)"""
    session["responses"] = []
    return redirect("/questions/0")


@app.route("/questions/<int:question_id>")
def survey(question_id):
    """Display survey pages"""

    survey = surveys.satisfaction_survey
    responses = session["responses"]
    breakpoint()
    if question_id == len(survey.questions) and question_id == len(responses):
        """Survey complete!"""
        return redirect("/thank-you")
    elif question_id > len(survey.questions):
        """Out of range"""
        flash(">:( You're trying to access an invalid question")
        return redirect("/questions/" + str(len(responses)))
    else:
        return render_template(
            "questions.jinja-html",
            id=question_id,
            title=survey.title,
            instructions=survey.instructions,
            question=survey.questions[question_id].question,
            choices=survey.questions[question_id].choices,
        )


@app.route("/answers", methods=["POST"])
def record_answer():
    """Save the posted response and redirect"""

    survey = surveys.satisfaction_survey
    responses = session["responses"]
    question_id = int(request.form["id"])
    response = request.form.get("choice")
    responses.append(response)
    session["responses"] = responses
    next_question = question_id + 1
    return redirect("/questions/" + str(next_question))


@app.route("/thank-you")
def thankyou():
    """Diplay thank-you page for completing the survey"""

    return render_template("/thank-you.jinja-html")
