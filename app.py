from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESONSES_KEY = "response"
responses = []

@app.route('/')
def show_title_page():
    ''' render a page that shows the user the title of the survey, 
    the instructions, and a button to start the survey. '''

    # make sure responses empty when survey starts

    title = survey.title
    instructions = survey.instructions
    

    return render_template("survey_start.html",
        survey_title=title, 
        survey_instructions=instructions)


@app.route('/begin', methods=["POST"])
def begin():
    """ When start button clicked, directs used to first question in survey """
    
    session[RESONSES_KEY] = []
    return redirect('/questions/0')
    

@app.route('/questions/<int:qnum>')
def generate_question(qnum):
    ''' generate current question and render a page with response options '''
    
    answers = session[RESONSES_KEY]

    #if responses collected already, redirect to completion page
    if len(answers) == len(survey.questions):
        flash("You've already completed the survey")
        return redirect('/complete')

    #if user tries to answer questions out of order redirects them to correct question
    if not len(answers) == qnum:
        flash("Please answer questions in order")
        return redirect(f'/questions/{len(answers)}')


    return render_template('question.html', question=survey.questions[qnum])


@app.route('/answer', methods=["POST"])
def store_answer():
    ''' stores user answer from previous question and redirect to next question or completion page '''
    
    answer = request.form['answer']

    # append answer to session list of all answers
    answers = session[RESONSES_KEY]
    answers.append(answer)
    session[RESONSES_KEY] = answers

    #print(session["responses"])

    # if len(responses) = total questions
        # go to completion 
    if len(answers) == len(survey.questions):
        return redirect('/complete')
    
    # if len(responses) < total questions
        #  go to next question  
    return redirect(f"/questions/{len(answers)}")
    
@app.route('/complete')
def complete():

     return render_template('completion.html')

