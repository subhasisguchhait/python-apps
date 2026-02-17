# app/resources/users.py
from flask import g
from flask_smorest import Blueprint, abort
from sqlalchemy import select, text

from ..models import User
from ..schemas import UserSchema, UserCreateSchema, UserUpdateSchema

users_blp = Blueprint(
    "users",
    "users",
    url_prefix="/api/v1/users",
    description="User CRUD operations",
)


@users_blp.get("/")
@users_blp.response(200, UserSchema(many=True))
def list_users():
    """List users ordered by id."""
    db = g.db
    # stmt = select(User).order_by(User.id.asc())
    # return db.execute(stmt).scalars().all()

    stmt = text("SELECT u.full_name FROM users u") 
    result = db.execute(stmt).mappings()
    return [dict(row) for row in result]


@users_blp.get("/<int:user_id>")
@users_blp.response(200, UserSchema)
def get_user(user_id: int):
    """Fetch a single user by primary key."""
    db = g.db
    # user = db.get(User, user_id)
    # if not user:
    #     abort(404, message="User not found")
    # return user

    stmt = text("SELECT u.full_name, u.email FROM users u where u.id=:id") 
    result = db.execute(stmt, {"id":user_id}).mappings()
    result = [dict(row) for row in result][0]  # Get the first (and only) result as a dict as this is not a list of users but a single user
    return result


@users_blp.post("/")
@users_blp.arguments(UserCreateSchema)
@users_blp.response(201, UserSchema)
def create_user(payload):
    """Create a user."""
    db = g.db

    # # Check email uniqueness (DB constraint remains the real authority)
    # exists_stmt = select(User).where(User.email == payload["email"])
    # if db.execute(exists_stmt).scalars().first():
    #     abort(409, message="Email already exists")

    # user = User(full_name=payload["full_name"], email=payload["email"])
    # db.add(user)
    # db.commit()
    # db.refresh(user)  # loads generated id
    # return user

    stmt = text("SELECT u.full_name, u.email FROM users u where u.email=:email") 
    result = db.execute(stmt, {"email":payload["email"]}).mappings().first()
    if result:
        abort(409, message="Email already exists")
    
    stmt = text("INSERT INTO users (full_name, email) VALUES (:full_name, :email) RETURNING id, full_name, email")
    result = db.execute(stmt, {"full_name":payload["full_name"], "email":payload["email"]}).mappings().first()
    db.commit() 
    return dict(result)


@users_blp.put("/<int:user_id>")
@users_blp.arguments(UserUpdateSchema)
@users_blp.response(200, UserSchema)
def update_user(data, user_id: int):
    """Update a user (partial update allowed)."""
    db = g.db

    # user = db.get(User, user_id)
    # if not user:
    #     abort(404, message="User not found")

    # # If email is changing, enforce uniqueness
    # if "email" in payload and payload["email"] != user.email:
    #     exists_stmt = select(User).where(User.email == payload["email"])
    #     if db.execute(exists_stmt).scalars().first():
    #         abort(409, message="Email already exists")

    # for k, v in payload.items():
    #     setattr(user, k, v)

    # db.commit()
    # db.refresh(user)
    # return user

    stmt = text("SELECT u.full_name, u.email FROM users u where u.email=:email") 
    result = db.execute(stmt, {"email":data["email"]}).mappings().first()
    if result:
        abort(409, message="Email already exists")

    stmt = text("UPDATE users SET full_name=:full_name, email=:email WHERE id=:id")
    result = db.execute(stmt, {"full_name":data["full_name"], "email":data["email"], "id":user_id})
    db.commit()
    
    stmt = text("SELECT u.full_name, u.email FROM users u where u.email=:email") 
    result = db.execute(stmt, {"email":data["email"]}).mappings().first()
    return dict(result)
    

@users_blp.delete("/<int:user_id>")
@users_blp.response(204)
def delete_user(user_id: int):
    """Delete a user."""
    db = g.db

    # user = db.get(User, user_id)
    # if not user:
    #     abort(404, message="User not found")

    # db.delete(user)
    # db.commit()
    # return ""

    stmt = text("SELECT u.full_name, u.email FROM users u where u.id=:id") 
    result = db.execute(stmt, {"id":user_id}).mappings().first()    
    if not result:
        abort(404, message="User not found")
    
    stmt = text("DELETE FROM users WHERE id=:id")
    db.execute(stmt, {"id":user_id})
    db.commit()
    return ""