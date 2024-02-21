from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, URL
from models import Base
import os





url = URL.create(
    drivername="postgresql+psycopg2",  # driver name = postgresql + the library we are using (psycopg2)
    username=os['POSTGRES_USER'],
    password=os['POSTGRES_PASSWORD'],
    host=os['DATABASE_HOST'],
    database=os['POSTGRES_DB'],
    port=5432
)
config.set_main_option('sqlalchemy.url', str(url))

engine = create_engine(url) # skipped echo=True to avoid printing out all the SQL commands

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

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
      