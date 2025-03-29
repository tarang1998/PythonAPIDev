from flask import Flask, abort
from flask.views import MethodView
from flask_smorest import Api, Blueprint
from datetime import datetime, timezone
from marshmallow import Schema, fields
import enum 
import uuid

app = Flask(__name__)


class ApiConfig:
    API_TITLE = "Todo API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"  # URL for the Swagger UI
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_REDOC_PATH = "/redoc"  # URL for the ReDoc documentation
    OPENAPI_REDOC_URL = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"  # URL for the ReDoc JS


app.config.from_object(ApiConfig)

api = Api(app)

todo = Blueprint('todo', "todo" , url_prefix='/todo', description='Operations on todo items')


tasks = [{
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "title": "Buy groceries",
    "created_at": datetime.now(timezone.utc),
    "completed": False

}]  # This will hold our todo items


class CreateTask(Schema):
    title = fields.Str(required=True, description="The title of the task")   

class UpdateTask(Schema):
    title = fields.Str(required=False, description="The title of the task")
    completed = fields.Boolean(required=False, description="Status of the task") 

class Task(UpdateTask):
    id = fields.Str(required=True, description="The unique identifier of the task")
    created_at = fields.DateTime(required=True, description="The creation date of the task")

class ListTasks(Schema):
    tasks = fields.List(fields.Nested(Task), description="List of tasks", required=True)

class SortByEnum(enum.Enum):
    title = "title"
    created_at = "created_at"

class SortDirectioEnum(enum.Enum):
    asc = "asc"
    desc = "desc"

class ListTaskParameters(Schema):
    order_by = fields.Enum(SortByEnum, default=SortByEnum.created_at, description="Field to sort the tasks by")
    order = fields.Enum(SortDirectioEnum, default=SortDirectioEnum.asc, description="Sort direction (asc or desc)")


@todo.route('/tasks',)
class TodoCollection(MethodView):

    @todo.arguments(ListTaskParameters, location="query")
    @todo.response(status_code=200,schema=ListTasks)
    def get(self,params):
        print("Getting tasks...")

        # Apply default values if not provided in the query
        order_by = params.get('order_by', SortByEnum.created_at).value
        order = params.get('order', SortDirectioEnum.asc).value

       
        return {"tasks": sorted(tasks, key=lambda x: x[order_by], 
                                reverse=(order == SortDirectioEnum.desc.value))}  # Sort tasks based on the provided parameters

    @todo.arguments(CreateTask)
    @todo.response(status_code=201,schema=Task)
    def post(self, task):

        task["id"] = str(uuid.uuid4())  # Generate a unique ID for the task
        task["created_at"] = datetime.now(timezone.utc)
        task["completed"] = False  # Default to not completed
        tasks.append(task)  # Add the new task to the list
        print("Task added:", task)
        return task

@todo.route('/tasks/<string:task_id>')
class TodoTask(MethodView):

    @todo.response(status_code=200, schema=Task)
    def get(self,task_id):
        for task in tasks:
            if task["id"] == task_id:
                return task
        abort(404, description=f"Task with ID {task_id} not found")  # Return a 404 error if the task is not found

    @todo.arguments(UpdateTask)
    @todo.response(status_code=200, schema=Task)
    def put(self,payload,task_id):
        for task in tasks:
            if task["id"] == task_id:
                # Update the task with the provided data
                if "title" in payload:
                    task["title"] = payload["title"]
                if "completed" in payload:
                    task["completed"] = payload["completed"]
                return task
        abort(404, description=f"Task with ID {task_id} not found")  # Return a 404 error if the task is not found

    @todo.response(status_code=204, schema=Task)
    def delete(self,task_id):

        for index, task in enumerate(tasks):
            if task["id"] == task_id:
                del tasks[index]
                return task  
                # 204 No Content response is expected to have no body. 
                # According to the HTTP specification, a 204 status code means "No Content," so Flask-Smorest automatically suppresses any response body when you use 
        abort(404, description=f"Task with ID {task_id} not found")  # Return a 404 error if the task is not found 


api.register_blueprint(todo)




@app.route('/')
def index():
    return "Hello, World!"