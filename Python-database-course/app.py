from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, URL, or_
from models import Base, User
from typing import List
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

# Base.metadata.drop_all(engine)
# target_metadata = Base.metadata
# Base.metadata.create_all(engine)

# a sessionmaker(), also in the same scope as the engine
session_pool = sessionmaker(bind=engine)


class Repo:
    def __init__(self, session: Session):
        self.session = session

    def add_user(
        self,
        telegram_id: int,
        full_name: str,
        language_code: str,
        user_name: str = None,
        referrer_id: int = None,
    ):
        stmt = insert(User).values(
            telegram_id=telegram_id,
            full_name=full_name,
            user_name=user_name,
            language_code=language_code,
            referrer_id=referrer_id,
        )
        self.session.execute(stmt)
        self.session.commit()

    def get_user_by_id(self, telegram_id: int) -> User:
        # Notice that you should pass the comparison-like arguments
        # to WHERE statement, as you can see below, we are using
        # `User.telegram_id == telegram_id` instead of
        # `User.telegram_id = telegram_id`
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = self.session.execute(stmt)
        # After we get the result of our statement execution, we need to
        # define HOW we want to get the data. In most cases you want to
        # get the object(s) or only one value. To retrieve the object
        # itself, we call the `scalars` method of our result. Then we
        # have to define HOW MANY records you want to get. It can be
        # `first` object, `one` (raises an error if there are not
        # exactly one row retrieved)) / `one_or_none` and so on.
        return result.scalars().first()

    def get_all_users_simple(self) -> List[User]:
        stmt = select(User)
        result = self.session.execute(stmt)
        return result.scalars().all()

    def get_all_users_advanced(self) -> List[User]:
        stmt = select(
            User,
        ).where(
            # OR clauses' syntax is explicit-only, unlike the AND clause.
            # You can pass each argument of OR statement as arguments to
            # `sqlalchemy.or_` function, like on the example below
            or_(
                User.language_code == 'en',
                User.language_code == 'uk',
            ),
            # Each argument that you pass to `where` method of the Select object
            # considered as an argument of AND statement
            User.user_name.ilike('%john%'),
        ).order_by(
            User.created_at.desc(),
        ).limit(
            10,
        ).having(
            User.telegram_id > 0,
        ).group_by(
            User.telegram_id,
        )
        result = self.session.execute(stmt)
        return result.scalars().all()

    def get_user_language(self, telegram_id: int) -> str:
        stmt = select(User.language_code).where(
            User.telegram_id == telegram_id)
        result = self.session.execute(stmt)
        return result.scalar()


with session_pool() as session:
    repo = Repo(session)
    user = repo.get_user_by_id(1)
    print(
        f'User: {user.telegram_id} '
        f'Full name: {user.full_name} '
        f'Username: {user.user_name} '
        f'Language code: {user.language_code}'
    )
    all_users = repo.get_all_users_simple()
    print(all_users)
    users = repo.get_all_users_advanced()
    print(users)
    user_language = repo.get_user_language(1)
    print(user_language)
