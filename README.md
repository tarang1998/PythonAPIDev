# PythonAPIDev

## [1> Social App API's using FAST API, SQLAlchemy and PostgreSQL](./social_app/)

API's for a social media application

### Tech Stack  
- Python 
- [FAST API](https://fastapi.tiangolo.com/tutorial/)
- Pydantic
- ORM : SQLAlchemy
- Alembic
- Database : PostgreSQL

### Running the project 

- Create the python virtual environment 
```
python3 -m venv venv 
```

- Activate the virtual environment (in Windows PowerShell)
```
venv\Scripts\activate.ps1
```

- Download all the requirements
```
pip install -r requirements.txt
```

- Run the FASTAPI live server for the social media app
```
fastapi dev social_app/main.py
```

- The postman collection for the API's - [Social App API](./social_app/Social%20App%20-%20FAST%20API.postman_collection.json)

- Postman collection environments : [Dev](./social_app/Dev-%20fastAPISocialAPP.postman_environment.json)




## [2> Fund Manager API's using Flask, SQLAlchemy and PostgreSQL](./fund_manager/)

### Tech Stack 
- Python
- Flask 
- SQLAlchemy
- PostgreSQL

### Running the project 

- Create the python virtual environment 
```
python3 -m venv venv 
```

- Activate the virtual environment (in Windows PowerShell)
```
venv\Scripts\activate.ps1
```

- Download all the requirements
```
pip install -r requirements.txt
```

- Create the database tables 
```
cd fundmanager
flask shell
In the shell run the command : db.create_all()
```

- Run the flask app
```
flask run --port 8000
```

## [3> Flask Documentation Tutorial](./flask-tutorial/)

### Running the project 

- Run the flask application
```
cd flask-tutorial
flask --app flaskr run --debug
```

- Initialize the Database file 
```
flask --app flaskr init-db
```

## [4> TODO App](./todo-apis/)

### Running the project 

```
cd todo-apis
flask run --port 8000

```

## [5> Patient Management System](./patient-management/)

### Running the project 

```
cd patient-management 
python3 -m venv venv 
venv\Scripts\activate.ps1
pip install -r requirements.txt
flask run --port 8000
```



## Resources 

- [Python API Development - Comprehensive Course for Beginners](https://www.youtube.com/watch?v=0sOvCWFmrtA)
- [Python Flask CRUD API - SQLAlchemy & Postgres](https://www.youtube.com/watch?v=Yh0uwzQ-TrE&t)
- [Build APIs with Flask (the right way)](https://www.youtube.com/watch?v=mt-0F_5KvQw)
- [Build and Deploy a Complete REST API with Python Flask Tutorial.](https://www.youtube.com/watch?v=WFzRy8KVcrM&t)
- [Flask documentation](https://flask.palletsprojects.com/en/stable/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status)
- [How To Kill Port 8000](https://canonigod.medium.com/how-to-kill-port-8000-c251b0e7017d)
- [PostgreSQL Data types](https://www.postgresql.org/docs/current/datatype.html)
