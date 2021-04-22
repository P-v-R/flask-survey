from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES = []

@app.route('/')
def show_title_page():
    ''' render a page that shows the user the title of the survey, 
    the instructions, and a button to start the survey. '''

    # make sure responses empty when survey starts
    RESPONSES=[]

    title = survey.title
    instructions = survey.instructions
    

    return render_template("survey_start.html",
    survey_title = title, 
    survey_instructions = instructions )


@app.route('/begin', methods=["POST"])
def begin():
    """ When start button clicked, directs used to first question in survey """
    session['answers'] = []
    
    return redirect('/questions/0')
    

@app.route('/questions/<int:qnum>')
def generate_question(qnum):
    ''' generate current question and render a page with response options '''

    return render_template('question.html', question=survey.questions[qnum])



@app.route('/answer', methods=["POST"])
def store_answer():
    ''' stores user answer from previous question and redirect to next question '''
    
    answer = request.form['answer']
    RESPONSES.append(answer)
    print(RESPONSES)
    if len(RESPONSES) == len(survey.questions):
        breakpoint()
    
    # if len(RESPONSES) < total questions 
    return redirect(f"/questions/{len(RESPONSES)}")
    # if len(RESPONSES) > total questions
        # go to completion 



