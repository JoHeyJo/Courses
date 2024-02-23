from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, URL
from models import Base, User
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
Base.metadata.create_all(engine)

# a sessionmaker(), also in the same scope as the engine
session_pool = sessionmaker(bind=engine)

# Base.drop_all(engine)
# class Repo:
#     def __init__(self, session: Session):
#         self.session = session

#     def add_user(
#         self,
#         telegram_id: int,
#         full_name: str,
#         language_code: str,
#         user_name: str = None,
#         referrer_id: int = None,
#     ):
#         stmt = insert(User).values(
#             telegram_id=telegram_id,
#             full_name=full_name,
#             user_name=user_name,
#             language_code=language_code,
#             referrer_id=referrer_id,
#         )
#         self.session.execute(stmt)
#         self.session.commit()


# with session_pool() as session:
#     repo = Repo(session)
#     repo.add_user(
#         telegram_id=1,
#         full_name='John Doe',
#         user_name='johnny',
#         language_code='en',
#     )
