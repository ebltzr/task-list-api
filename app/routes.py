from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

def validate_task(task_id):
    try:
        task_id=int(task_id)
    except:
        abort(make_response({'msg':f'Invalid id {task_id}'},400))
        
    task=Task.query.get(task_id)
    
    return task if task else abort(make_response({'msg':
        f'No task with id{task_id}'}, 404))

task_bp = Blueprint("tasks",__name__,url_prefix="/tasks")


# CREATE A TASK --- PASSED
@task_bp.route("",methods=['POST'])
def create_task():
    request_body=request.get_json()
    new_task=Task(
        title=request_body['title'],
        description=request_body['description'],
        completed_at=request_body['completed_at'] if 'completed_at' in request_body else None
    )
    
    db.session.add(new_task)
    db.session.commit()

    return {
            "task": new_task.to_dict()
        }, 201
    

# GET TASKS: NO SAVED TASKS --- PASSED
@task_bp.route("",methods=['GET'])
def get_all_tasks():
    response=[]
    title_query=request.args.get("title")
    
    if title_query is None:
        tasks=Task.query.all()
    else:
        tasks=Task.query.filter_by(title=title_query).all()
        
    for task in tasks:
        response.append(task.to_dict())
        
    return jsonify(response),200   


# GET ONE TASK: ONE SAVED TASK
@task_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    task=validate_task(task_id)
    return {
            "task": task.to_dict()
        }, 200


#UPDATE TASK 
@task_bp.route("/<task_id>", methods=['PUT'])
def update_task(task_id):
    task=validate_task(task_id)
    request_data = request.get_json()

    task.title = request_data["title"] if 'title' in request_data else task.title
    task.description = request_data["description"] if 'description' in request_data else task.description
    task.completed_at = request_data['completed_at'] if 'completed_at' in request_data else task.completed_at

    db.session.commit()
    return {
            "task": task.to_dict()
        }, 200