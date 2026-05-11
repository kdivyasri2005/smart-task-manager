from extensions import socketio
from flask import session
from flask import Blueprint, request, jsonify, render_template, redirect
from flask_login import login_required, current_user

from db import db
from models.models import Task

import pandas as pd
import numpy as np

task = Blueprint('task', __name__)


# ✅ ADD TASK PAGE

@task.route('/add_task_page')
@login_required
def add_task_page():

    return render_template('add_task.html')


# ✅ ADD TASK

@task.route('/add_task', methods=['POST'])
@login_required
def add_task():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "No JSON data received"
        }), 400

    new_task = Task(
        title=data.get('title'),
        description=data.get('description'),
        priority=data.get('priority'),
        status=data.get('status'),
        user_id=current_user.id
    )

    db.session.add(new_task)

    db.session.commit()

    # ✅ WEBSOCKET NOTIFICATION

    socketio.emit(
        'task_notification',
        {
            'message': '✅ Task Added Successfully'
        }
    )

    return jsonify({
        "message": "Task added successfully"
    }), 201


# ✅ GET ALL TASKS

@task.route('/get_tasks', methods=['GET'])
@login_required
def get_tasks():

    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).all()

    task_list = []

    for t in tasks:

        task_list.append({

            "id": t.id,

            "title": t.title,

            "description": t.description,

            "priority": t.priority,

            "status": t.status,

            "created_date":
            t.created_date.strftime('%Y-%m-%d')
        })

    return jsonify(task_list), 200


# ✅ ANALYTICS

@task.route('/task_analytics', methods=['GET'])
@login_required
def task_analytics():

    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).all()

    task_data = []

    for t in tasks:

        task_data.append({

            "title": t.title,
            "status": t.status
        })

    df = pd.DataFrame(task_data)

    total_tasks = len(df)

    if total_tasks == 0:

        completed_tasks = 0
        pending_tasks = 0
        completion_percentage = 0

    else:

        completed_tasks = np.sum(
            df['status'] == 'Completed'
        )

        pending_tasks = np.sum(
            df['status'] == 'Pending'
        )

        completion_percentage = round(
            (completed_tasks / total_tasks) * 100,
            2
        )

    return jsonify({

        "total_tasks": int(total_tasks),

        "completed_tasks":
        int(completed_tasks),

        "pending_tasks":
        int(pending_tasks),

        "completion_percentage":
        float(completion_percentage)

    })


# ✅ UPDATE PAGE

@task.route('/update_task_page/<int:id>')
@login_required
def update_task_page(id):

    task_item = db.session.get(Task, id)

    if not task_item:

        return "Task not found"

    return render_template(
        'update_task.html',
        task=task_item
    )


# ✅ UPDATE TASK

@task.route('/update_task/<int:id>', methods=['POST'])
@login_required
def update_task(id):

    task_item = db.session.get(Task, id)

    if not task_item:

        return "Task not found"

    task_item.title = request.form['title']

    task_item.description = request.form['description']

    task_item.priority = request.form['priority']

    task_item.status = request.form['status']

    db.session.commit()

    # ✅ SAVE MESSAGE FOR DASHBOARD NOTIFICATION

    session['notification'] = "Task Updated Successfully"

    # ✅ WEBSOCKET NOTIFICATION

    socketio.emit(
        'task_notification',
        {
            'message': 'Task Updated Successfully'
        }
    )

    return redirect('/dashboard')


# ✅ DELETE TASK

@task.route('/delete_task/<int:id>', methods=['DELETE'])
@login_required
def delete_task(id):

    task_item = db.session.get(Task, id)

    if not task_item:

        return jsonify({
            "error": "Task not found"
        }), 404

    db.session.delete(task_item)

    db.session.commit()

    # ✅ WEBSOCKET NOTIFICATION

    socketio.emit(
        'task_notification',
        {
            'message': '🗑️ Task Deleted Successfully'
        }
    )

    return jsonify({
        "message": "Task deleted successfully"
    }), 200

# ✅ GET SESSION NOTIFICATION

@task.route('/get_notification')
@login_required
def get_notification():

    message = session.pop('notification', None)

    return jsonify({
        "message": message
    })