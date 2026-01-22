from sqlalchemy import create_engine, Column, Integer, String, select, update, delete, text
from sqlalchemy.orm import declarative_base, sessionmaker
from contextlib import contextmanager


engine = create_engine('sqlite:///./example.db', echo=False)
Base = declarative_base()

# Create a configured "Session" class
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# def get_db():
#     with Session() as session:
#         yield session


@contextmanager
def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()
        
# Define ORM models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    email_address = Column(String)


### When using FastAPI or other frameworks, you would typically manage sessions using dependency injection.


# #Case1: Simple select using the ORM models
# session = Session()
# result = session.query(User).all()
# for row in result:
#     print(row.name, row.age)
# session.close()

# #Case2: Simple select using the ORM models - using context manager
with get_db() as session:
    result = session.query(User).all()
    for row in result:
        print(row.name, row.age)


# #Case3: ORM models - join with another table
with get_db() as session:
    result = session.query(User, Address).join(Address, User.id == Address.user_id).all()
    for user, address in result:  #key difference is here
        print(user.name, user.age, address.email_address)


# #Case4: ORM models - join with another table and select specific columns
with get_db() as session:
    result = session.query(User.name, User.age, Address.email_address).join(Address, User.id == Address.user_id).all()
    for row in result:
        print(row.name, row.age, row.email_address)


# #Case5: Using session.query construct with ORM models - multiple columns
with get_db() as session:
    result = session.query(User.name, User.age, Address.email_address).join(Address, User.id == Address.user_id).all()
    for row in result:
        print(row.name, row.age, row.email_address)


# #Case6: Using session.execute construct with ORM models - multiple columns
with get_db() as session:
    result = session.execute(select(User.name, User.age, Address.email_address).join(Address, User.id == Address.user_id)).all()
    for row in result:
        print(row.name, row.age, row.email_address)  


# #Case7: Inserting data using ORM models
with get_db() as session:
    session.add(User(name="Subhasis", age=40))
    session.add(Address(user_id=3, email_address="subhasis@example.com"))
    session.commit()

# #Case8: filter data
with get_db() as session:
    result = session.execute(select(User.name, User.age, Address.email_address).join(Address, User.id == Address.user_id).filter(User.age > 25)).all()
    for row in result:
        print(row.name, row.age, row.email_address)

# #Case9: update data (preferred: core-style update)
# with get_db() as session:
#     stmt = update(Address).where(Address.user_id == 3).values(email_address="subhasis_updated@example.com")
#     session.execute(stmt)
#     session.commit()

# #ORM-instance style (alternate)
with get_db() as session:
    addr = session.query(Address).filter(Address.user_id==3).first()
    if addr:
        addr.email_address = "subhasis_updated@example.com"
        session.commit()

# #Case9.1: Using session.query construct with ORM models
with get_db() as session:
    result = session.query(User.name, User.age, Address.email_address).join(Address, User.id == Address.user_id).all()
    for row in result:
        print(row.name, row.age, row.email_address)  

#Case10: delete data (preferred: core-style delete)
# with get_db() as session:
#     stmt = delete(Address).where(Address.user_id == 3)
#     session.execute(stmt)
#     session.commit()

# #ORM-instance style (alternate)
with get_db() as session:
    addr = session.query(Address).filter(Address.user_id==3).first()
    if addr:
        session.delete(addr)
        session.commit()

# #Case11: Using session.query construct with ORM models
with get_db() as session:
    result = session.query(User.name, User.age, Address.email_address).join(Address, User.id == Address.user_id).all()
    for row in result:
        print(row.name, row.age, row.email_address)  

# #Case12: Use raw SQL query 
with get_db() as session:
    stmt = text("SELECT u.name, u.age, a.email_address FROM users u JOIN addresses a ON u.id = a.user_id WHERE u.age > :age")
    result = session.execute(stmt, {"age": 25}).all()
    for row in result:
        print(row.name, row.age, row.email_address)


# #Case12: Use raw SQL query insert
with get_db() as session:
    stmt = text("INSERT INTO users (name, age) VALUES (:name, :age)")
    session.execute(stmt, {"name": "Charlie", "age": 28})
    session.commit()    

# #Case12: Use raw SQL query select to verify insert
with get_db() as session:
    stmt = text("SELECT name, age FROM users WHERE name = :name")
    result = session.execute(stmt, {"name": "Charlie"}).all()
    for row in result:
        print(row.name, row.age)

# #Case12: Use raw SQL query delete
with get_db() as session:
    stmt = text("DELETE FROM users WHERE name = :name")
    session.execute(stmt, {"name": "Charlie"})
    session.commit()

# #Case12: Use raw SQL query select to verify delete
with get_db() as session:
    stmt = text("SELECT u.name, u.age, a.email_address FROM users u JOIN addresses a ON u.id = a.user_id")
    result = session.execute(stmt).all()
    for row in result:
        print(row.name, row.age, row.email_address)