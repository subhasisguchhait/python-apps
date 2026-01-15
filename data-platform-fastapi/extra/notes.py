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
*** All folder are modules with __init__.py file


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
    - sample response for dataset creation to unsure endpoints are working
Now create a sqlite database (module - aiosqlite ) and connect the fastapi app to it
    - one engine per app
    - one session per request
    - use async session for non-blocking db operations
Create SQLAlchemy models for db tables
    - DatasetBase model for datasets table
    - Run as: python -m extra.create_tables
Now implement the /create dataset endpoint to save data to the db
    - use async db session
    - add, commit, refresh
Now implement the /list/all dataset endpoint to save data to the db
Now implement CRUD endpoints, will multiple update and delete endpoints

Now add authentication and authorization using JWT tokens
    - User registration and login endpoints
    
Sample request to create dataset:
{
  "name": "order1",
  "source": "s3://delta/bronze/order1.csv",
  "format": "csv",
  "owner": "finance"
}

uvicorn app.main:app --reload
'''



