from flask import Blueprint, jsonify, abort, make_response, request, current_app
import requests
from app import db

from app.models.goal import Goal
from .routes import get_task_from_db


goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

def get_goal_from_db(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({'msg': f'Invalid id {goal_id}'}, 400))
        
    goal = Goal.query.get(goal_id)

    return goal if goal else abort(make_response({'msg': f'No Goal with id: {goal_id}'}, 404))



@goal_bp.route("", methods=['POST'])
def create_goal():
    request_body = request.get_json()
    
    if 'title' not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_goal = Goal(
        title = request_body['title']
    )
    
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201
    

@goal_bp.route('', methods=['GET'])
def get_goals():
    response = []
    sort_goals = request.args.get("sort")
    if sort_goals == "asc":
        goals = Goal.query.order_by(Goal.title.asc()).all()
    elif sort_goals == "desc":
        goals = Goal.query.order_by(Goal.title.desc()).all()
    else:
        goals = Goal.query.all()

    for goal in goals:
        response.append(goal.to_dict())

    return jsonify(response), 200


@goal_bp.route("/<goal_id>", methods=['GET'])
def get_goal(goal_id):
    goal = get_goal_from_db(goal_id)
    
    return {
            "goal": goal.to_dict()
        }, 200


@goal_bp.route("/<goal_id>", methods=['PUT'])
def update_goal(goal_id):
    goal = get_goal_from_db(goal_id)
    request_data = request.get_json()

    goal.title = request_data["title"] if 'title' in request_data else goal.title
    # goal.description = request_data["description"] if 'description' in request_data else goal.description
    # goal.completed_at = request_data['completed_at'] if 'completed_at' in request_data else goal.completed_at

    db.session.commit()
    return {
            "goal": goal.to_dict()
        }, 200

@goal_bp.route('/<goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    goal_deleted = get_goal_from_db(goal_id)
    
    db.session.delete(goal_deleted)
    db.session.commit()
    
    return {
        "details":
            f'goal {goal_id} \"{goal_deleted.title}\" successfully deleted'
        }
    

# WAVE 3 - MARK COMPLETE --- PASSED
@goal_bp.route('/<goal_id>/mark_complete', methods=['PATCH'])
def mark_complete(goal_id):
    goal = get_goal_from_db(goal_id)
    # goal.completed_at= datetime.now()

    db.session.commit()
    
    url = 'https://slack.com/api/chat.postMessage'
    myobj = {'text': f'Someone just completed the goal {goal.title}', 'channel': 'goal-notifications'}

    requests.post(url, data = myobj, headers = {"Authorization": f"Bearer {current_app.config['SLACK_API_URI']}"})
    
    return {"goal": goal.to_dict()}, 200
    

@goal_bp.route('/<goal_id>/mark_incomplete', methods=['PATCH'])
def mark_incomplete(goal_id):
    goal = get_goal_from_db(goal_id)
    goal.completed_at = None
    
    db.session.commit()
    return {
            "goal": goal.to_dict()
        }, 200
    

@goal_bp.route("/<goal_id>/tasks", methods=['POST'])
def post_task_ids_to_goal(goal_id):

    goal = get_goal_from_db(goal_id)
    request_body = request.get_json()
    
    if 'task_ids' not in request_body or isinstance(request_body['tasks_ids'], list) :
        return {"details": "Invalid data"}, 400
    
    for task_id in request_body['task_ids']:
        task = get_task_from_db(task_id)
        task.goal = goal

    db.session.commit()
    
    return {
        'id': goal_id,
        'task_ids': request_body['task_ids']
    } , 201

