# PythonAPIDev

## Social App API's using FAST API, SQLAlchemy and PostgreSQL
API's for a social media application

### TechStack Used 
- Python 
- [FAST API](https://fastapi.tiangolo.com/tutorial/)
- Pydantic
- ORM : SQLAlchemy
- Alembic
- Database : PostgreSQL
- Docker

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

## Resources 

- [Python API Development - Comprehensive Course for Beginners](https://www.youtube.com/watch?v=0sOvCWFmrtA)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status)
- [How To Kill Port 8000](https://canonigod.medium.com/how-to-kill-port-8000-c251b0e7017d)
- [PostgreSQL Data types](https://www.postgresql.org/docs/current/datatype.html)

## Questions 
- HTTP Status Codes 
- What is CORS Issue
- Authentication in API - using JWT Token
- Advantages of using an ORM like SQL Alchemy 
- Using Alembic