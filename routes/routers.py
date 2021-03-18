import html
from datetime import datetime

from flask import request, render_template, jsonify

from main import app

import json


def load_data():
    """Load the data from the json file."""
    with open("./json/task.json") as task:
        return json.load(task)


def count_data():
    with open("./json/task.json") as task:
        return len(json.load(task))


def binary_search(x):
    tasked = load_data()
    low = 0
    high = count_data() - 1
    while low <= high:
        mid = (high + low)
        if int(tasked[mid]["id"]) < x:
            low = mid + 1
        elif int(tasked[mid]["id"]) > x:
            high = mid - 1
        else:
            return mid
    return -1


@app.route('/')
def home():
    tasked = load_data()
    return render_template('home.html', task=tasked)


@app.route('/add', methods=['POST'])
def add():
    task = request.get_json()
    error = 0
    tasked = load_data()
    try:
        task["task"]
    except:
        error = 1
    if error:
        return {"Error": "Please Fill all rhe required fields"}, 200, {'Content-type': 'application/json'}
    task["task"] = html.escape(task["task"])
    if count_data() == 0:
        id = 1
    else:
        id = int(tasked[count_data() - 1]["id"]) + 1
    date_created = datetime.now()
    date_created = date_created.strftime("%Y-%m-%d %H:%M:%S")
    newtask = {
        "id": id,
        "tasked": task["task"],
        "status": 0,
        "datecreated": date_created
    }
    with open("./json/task.json", 'w') as insertjson:
        tasked.append(newtask)
        json.dump(tasked, insertjson)
    return {"Success": "Successfully Added"}, 200, {'Content-type': 'application/json'}


@app.route('/checked/<int:id>', methods=['PUT'])
def checked(id):
    if id < 0:
        return {"Error": "Invalid Data"}, 200, {'Content-type': 'application/json'}
    index = binary_search(id)
    if index == -1:
        return {"Error": "Not a valid ID"}, 200, {'Content-type': 'application/json'}
    tasked = load_data()
    updatetask = {
        "id": id,
        "tasked": tasked[index]["tasked"],
        "status": 1,
        "datecreated": tasked[index]["datecreated"]
    }
    tasked[index] = updatetask
    with open("./json/task.json", 'w') as updatejson:
        json.dump(tasked, updatejson)
    return {"Success": "Successfully Updated"}, 200, {'Content-type': 'application/json'}



@app.route('/unchecked/<int:id>', methods=['PUT'])
def unchecked(id):
    if id < 0:
        return {"Error": "Invalid Data"}, 200, {'Content-type': 'application/json'}
    index = binary_search(id)
    if index == -1:
        return {"Error": "Not a valid ID"}, 200, {'Content-type': 'application/json'}
    tasked = load_data()
    updatetask = {
        "id": id,
        "tasked": tasked[index]["tasked"],
        "status": 0,
        "datecreated": tasked[index]["datecreated"]
    }
    tasked[index] = updatetask
    with open("./json/task.json", 'w') as updatejson:
        json.dump(tasked, updatejson)
    return {"Success": "Successfully Updated"}, 200, {'Content-type': 'application/json'}


@app.route('/remove/<int:id>', methods=['DELETE'])
def remove(id):
    if id < 0:
        return {"Error": "Invalid Data"}, 200, {'Content-type': 'application/json'}
    index = binary_search(id)
    if index == -1:
        return {"Error": "Not a valid ID"}, 200, {'Content-type': 'application/json'}
    tasked = load_data()
    del tasked[index]
    with open("./json/task.json", 'w') as updatejson:
        json.dump(tasked, updatejson)
    return {"Success": "Successfully Deleted"}, 200, {'Content-type': 'application/json'}


@app.route('/clear', methods=['DELETE'])
def clear():
    with open("./json/task.json", 'w') as updatejson:
        json.dump([], updatejson)
    return {"Success": "Successfully Deleted"}, 200, {'Content-type': 'application/json'}
