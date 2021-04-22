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

    
    title = survey.title
    instructions = survey.instructions


    return render_template("survey_start.html",
    survey_title = title, 
    survey_instructions = instructions )



# surveys = {
#     "satisfaction": satisfaction_survey,
#     "personality": personality_quiz,
# }
