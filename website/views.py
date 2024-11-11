from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import Event
from datetime import datetime
from . import db
import json
import lamini

lamini.api_key = "26c12df4ab71cc42b776ca900ee69743b7851e1bebdd1e791624c5e08b15f51d"

llm = lamini.Lamini("meta-llama/Meta-Llama-3.1-8B-Instruct")


def create_llama3_prompt(user_prompt: str, system_prompt: str = "") -> str:
    llama3_header = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
    llama3_middle = "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
    llama3_footer = "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    return llama3_header + system_prompt + llama3_middle + user_prompt + llama3_footer



views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        name = request.form.get('actName')
        dateStart = request.form.get('timestart')
        dateEnd = request.form.get('timeend')

        date_format = "%Y-%m-%dT%H:%M"
        py_dateStart = datetime.strptime(dateStart, date_format)
        py_dateEnd = datetime.strptime(dateEnd, date_format)
        
        priority = request.form.get('priority')
        mobility = request.form.get('mobility')

        if len(name) < 1 or len(priority) < 1 or len(mobility) < 1:
            flash("The new event has invalid input, please try again")

        else:
            new_event = Event(name = name, dateStart = py_dateStart, dateEnd = py_dateEnd, priority = priority, mobility = mobility, user_id = current_user.id)
            db.session.add(new_event) #adding the note to the database 
            db.session.commit()
            flash('Event added!', category='success')

    formatted_events = []

    for i in range(len(current_user.events)):
        newEvent = {}
        newEvent["title"] = current_user.events[i].name
        newEvent["start"] = current_user.events[i].dateStart.isoformat()
        newEvent["end"] = current_user.events[i].dateEnd.isoformat()
        formatted_events.append(newEvent)

    return render_template("calendar.html", user=current_user, events = formatted_events)


@views.route('/delete-event', methods = ["POST"])
def delete_event():
    name = request.form.get('actName')
    dateStart = request.form.get('timestart')

    date_format = "%Y-%m-%dT%H:%M"
    py_dateStart = datetime.strptime(dateStart, date_format)

    for i in range(len(current_user.events)):
        if (name == current_user.events[i].name and py_dateStart == current_user.events[i].dateStart):
            event = Event.query.get(current_user.events[i].id)
            db.session.delete(event)
            db.session.commit()
            flash("Succesfully Deleted Event", category = "success")
            return redirect("/")
    
    return redirect("/")
    
    
    



@views.route('/askAI', methods = ["POST"])
def ask_AI():
    uInput = request.form.get('chatInput') #Input obtained from the user

    formatted_events = [] #Este es el schedule actual

    for i in range(len(current_user.events)):
        newEvent = {}
        newEvent["title"] = current_user.events[i].name
        newEvent["start"] = current_user.events[i].dateStart.isoformat()
        newEvent["end"] = current_user.events[i].dateEnd.isoformat()
        formatted_events.append(newEvent)

    inputEvents = json.dumps(formatted_events)


    sysPrompt = "You are a specialist in time management and organization. You will be given a list of Python dictionaries and a Python dictionary. The list of Python dictionaries will represent an already existing schedule, and the single Python dictionary will represent a new event that I want to add to the schedule. Each event has the following categories: “Time” Represents the time of the event. “Activity” represents the name of the event. “Day” represents the day of the event. “Month” represents the month of the event. “Year” represents the year of the event. “Duration” represents how long the event lasts in minutes. “Priority” represents the priority of the event, which ranges from high, medium, and low. “Mobility” indicates if an event can be moved or not. The following is the list of Python dictionaries meant to represent the current schedule. Here is the current schedule:" + inputEvents

    uPrompt = "You have to give an answer in which information from activities is extracted from the vocabulary. Do not do more than 2000 characters and do not answer questions that are not related to the topic (remember that you jobs is only to be a specialist in time management), try to be concise and write in a natural language ( is for a human to read) and try to write an direct answer and do not show your process of getting that answer. Remember the properties like: “Time” represents the time of the event. “Activity” represents the name of the event. “Day” represents the day of the event. “Month” represents the month of the event. “Year” represents the year of the event. “Duration” represents how long the event lasts in minutes. “Priority” represents the priority of the event, which ranges from high, medium, and low. “Mobility” indicates if an event can be moved or not. Based on this, you can answer the following question provided by the user, which is:" + uInput 

    response = llm.generate(create_llama3_prompt(user_prompt=uPrompt, system_prompt=sysPrompt))


    flash(response) #This displays it to the site

    

    return redirect("/")





