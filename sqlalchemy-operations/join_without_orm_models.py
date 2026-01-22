from sqlalchemy import create_engine, Column, Integer, String, select, insert, update, delete, MetaData, Table, text
from sqlalchemy.orm import declarative_base, sessionmaker
from contextlib import contextmanager


engine = create_engine('sqlite:///./example.db', echo=False)


# Create a configured "Session" class
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Reflect existing tables
metadata=MetaData()
metadata.reflect(bind=engine)

# Access the tables dynamically
users = Table('users', metadata, autoload_with=engine)
addresses = Table('addresses', metadata, autoload_with=engine)

@contextmanager
def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()


#Case1: Delete data without ORM models
with get_db() as session:
    # stmt = delete(addresses).where(addresses.c.user_id == 3)
    stmt = delete(addresses)
    session.execute(stmt)
    session.commit()

    # stmt = delete(users).where(users.c.id == 3)
    stmt = delete(users)
    session.execute(stmt)
    session.commit()

#Case2: Insert data without ORM models
with get_db() as session:
    insert_user = users.insert().values([{"name": "Charlie", "age": 28},{"name": "Diana", "age": 22}])
    session.execute(insert_user)

    insert_address = addresses.insert().values([{"user_id": 1, "email_address": "charlie@example.com"}, {"user_id": 2, "email_address": "diana@example.com"}])
    session.execute(insert_address)

    insert_user = insert(users).values(name="Eve", age=35)
    session.execute(insert_user)
    session.commit()


# #Case3: Insert data without ORM models
with get_db() as session:
    stmt = insert(users).values(name="Subhasis", age=40)
    session.execute(stmt)
    session.commit()

    stmt = insert(addresses).values(user_id=3, email_address="subhasis@example.com")
    session.execute(stmt)
    session.commit()

#Case4: Update data without ORM models
with get_db() as session:
    stmt = update(addresses).where(addresses.c.user_id == 4).values(email_address="subhasis_updated@example.com")
    session.execute(stmt)
    session.commit()

# #Case5: Simple join without ORM models - execute select statement -- normal join 
# with get_db() as session:
#     stmt = select(users.c.name, users.c.age, addresses.c.email_address).\
#         join(addresses, users.c.id == addresses.c.user_id).\
#         where(users.c.age > 10)
#     result = session.execute(stmt).all()
#     for row in result:
#         print(row.name, row.age, row.email_address)

# #Case6: Simple join without ORM models - query construct  -- Left outer join select_from()
with get_db() as session:
    result = session.query(users.c.name, users.c.age, addresses.c.email_address).\
        select_from(users.outerjoin(addresses, users.c.id == addresses.c.user_id)).\
        filter(users.c.age > 10).all()
    for row in result:
        print(row.name, row.age, row.email_address)


#Case7:  Using raw SQL query delete
# with get_db() as session:
#     stmt = text("DELETE FROM addresses")
#     session.execute(stmt)
#     session.commit()

#     stmt = text("DELETE FROM users")
#     session.execute(stmt)
#     session.commit()

# #Case8: Use raw SQL query insert
with get_db() as session:
    stmt = text("INSERT INTO users (name, age) VALUES (:name, :age)")
    session.execute(stmt, {"name": "Bob", "age": 28})
    session.commit()    

# #Case9: Use raw SQL query select to verify insert
with get_db() as session:
    stmt = text("SELECT name, age FROM users WHERE name = :name")
    result = session.execute(stmt, {"name": "Bob"}).all()
    for row in result:
        print(row.name, row.age)

# #Case10: Use raw SQL query delete
with get_db() as session:
    stmt = text("DELETE FROM users WHERE name = :name")
    session.execute(stmt, {"name": "Bob"})
    session.commit()

# #Case11:  Using raw SQL query
with get_db() as session:
    stmt = text("SELECT u.id , u.name, u.age, a.user_id as address_id, a.email_address FROM users u left JOIN addresses a ON u.id = a.user_id")
    result = session.execute(stmt).all()
    for row in result:
        print(row.id, row.name, row.age, row.address_id, row.email_address)

# #Case12:  Using raw SQL query - bind parameters
with get_db() as session:
    stmt = text("SELECT u.name, u.age, a.user_id as address_id, a.email_address FROM users u JOIN addresses a ON u.id = a.user_id WHERE u.age > :age")
    result = session.execute(stmt, {"age": 25}).all()
    for row in result:
        print(row.name, row.age, row.address_id, row.email_address)

