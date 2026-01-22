from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///./example.db', echo=True)

# Reflect existing tables
metadata=MetaData()
metadata.reflect(bind=engine)

# Access the tables dynamically
users_table = Table('users', metadata, autoload_with=engine)
addresses_table = Table('addresses', metadata, autoload_with=engine)

# Insert data into users table
with engine.connect() as connection:
    insert_user = users_table.insert().values([{"name": "Alice", "age": 30},{"name": "Bob", "age": 25}])
    connection.execute(insert_user)

    insert_address = addresses_table.insert().values([{"user_id": 1, "email_address": "alice@example.com"},{"user_id": 2, "email_address": "bob@example.com"}])
    connection.execute(insert_address)

    connection.commit()

print("Data inserted successfully.")

#select data from users table
with engine.connect() as connection:
    select_users = users_table.select()
    result = connection.execute(select_users).all()
    for row in result:
        print(row)