from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, URL
from models import Base
from dotenv import load_dotenv
import os
load_dotenv()

url = URL.create(
    drivername="postgresql+psycopg2",  # driver name = postgresql + the library we are using (psycopg2)
    username=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host=os.environ['DATABASE_HOST'],
    database=os.environ['POSTGRES_DB'],
    port=5432
)


engine = create_engine(url) # skipped echo=True to avoid printing out all the SQL commands

Base.metadata.drop_all(engine)
# target_metadata = Base.metadata
# Base.metadata.create_all(engine)

# a sessionmaker(), also in the same scope as the engine
session_pool = sessionmaker(bind=engine)
# or you can name it `session_pool` or whatever you want

# we can now construct a Session() without needing to pass the
# engine each time
# with session_pool() as session:
    # query = text("""
    # INSERT INTO users (telegram_id, full_name, username, language_code, referrer_id)
    # VALUES (1, 'John Doe', 'johndoe', 'en', NULL),
    #           (2, 'Jane Doe', 'janedoe', 'en', 1);
    # """)
    # session.execute(query)
    # session.commit()

    # select_query = text("""
    # SELECT * FROM USERS
    # """)

    # result = session.execute(select_query)
    # for row in result:
    #   print(row)
# closes the session after exiting the context manager.
      