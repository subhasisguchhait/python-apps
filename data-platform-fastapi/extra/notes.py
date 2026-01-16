'''
*** requirements.txt ***
fastapi
uvicorn
asyncio
aiosqlite
pydantic
python-multipart
python-dotenv
python-jose
passlib
aragon2-cffi [avoid bcrypt as it has limitation on 72 characters for hashing passwords]
'''

'''
*** All folder are modules with __init__.py files ***
*** How to build the project: ***

Create a fastapi app
    - Add basic routes (/ and /health)
Pydantic models are for data validation and serialization 
Schemas define the structure of request and response data of the API endpoints
    - DatasetCreate, DatasetResponse, DatasetUpdate, DatasetMultipleUpdate
Use APIRouter for modular route management
Use async def for asynchronous endpoints

Create endpoints for creating datasets
    - POST /datasets/create
    - include the datasets router in the main app with a versioned prefix /api/v1
    - sample response for dataset creation to ensure endpoints are working

Create a sqlite database (module - aiosqlite ) and connect the fastapi app to it
    - one engine per app
    - one session per request
    - use async session for non-blocking db operations

Create SQLAlchemy models for db tables
    - DatasetBase model for datasets table
    - Run as: python -m extra.create_tables

Implement the /create dataset endpoint to save data to the db
    - use async db session
    - add, commit, refresh

Implement the /list/all dataset endpoint to save data to the db

Implement CRUD endpoints, will multiple update and delete endpoints

Add authentication and authorization using JWT tokens

    - Token generation - create_access_token and verify_password, hash_password functions - security.py
    - User model and schemas for db and data validation  - user.py
    - Create User table in the db - Make to sure to run create_tables.py again and from the root folder
    - Create user registration and login endpoints - auth.py
    - Register auth router in the main app with versioned prefix /api/v1
    - Create dependencies to get_current_user from token - deps.py
    - Protect dataset endpoints to allow only authenticated users
    - OAuth2PasswordRequestForm = Depends() for login form data from swagger ui
        - if not using form data, use pydantic model for login request body - ex - UserCreate model can be reused

        
For background processing jobs          
    - Create Job model and JobResponse schema - job.py
    - Create jobs table in the db - Make to sure to run create_tables.py again and from the root folder
    - Background Processing function to simulate dataset processing - services/processing.py
        - Never put this in the route handler directly as it will block the main event loop
    - Create job creation endpoint that starts a background task to process a dataset
    - Protect job endpoints to allow only authenticated users
    - Register jobs router in the main app with versioned prefix /api/v1



Sample request to create dataset:
{
  "name": "order1",
  "source": "s3://delta/bronze/order1.csv",
  "format": "csv",
  "owner": "finance"
}

uvicorn app.main:app --reload
'''



