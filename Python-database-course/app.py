import random
import sqlalchemy
from faker import Faker
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, URL, or_
from models import Base, User, Order, Product, OrderProduct
from typing import List
from dotenv import load_dotenv
import os
load_dotenv()
print('>>>>>>>',sqlalchemy.__version__) # version 2.0.4
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

    def get_all_user_orders_user_full(self, telegram_id: int):
        stmt = (
            select(Order, User).join(User.orders).where(
                User.telegram_id == telegram_id)
        )
        # NOTICE: Since we are joining two tables, we won't use `.scalars()` method.
        # Usually we want to use scalars if we are joining multiple tables or
        # when you use `.label()` method to retrieve some specific column etc.
        result = self.session.execute(stmt)
        return result.all()

    def get_all_user_orders_user_only_user_name(self, telegram_id: int):
        stmt = (
            select(Order, User.user_name).join(User.orders).where(
                User.telegram_id == telegram_id)
        )
        result = self.session.execute(stmt)
        return result.all()


with session_pool() as session:
    repo = Repo(session)
    user_orders = repo.get_all_user_orders_user_full(telegram_id=4104)
    # You have two ways of accessing retrieved data, first is like below:
    for order, user in user_orders:
        print(f'Order: {order.order_id} - {user.full_name}')
    print('=============')
    # Second is like next:
    for row in user_orders:
        print(f'Order: {row.Order.order_id} - {row.User.full_name}')
    print('=============')
    # In the next two examples you can see how to access your data when
    # you didn't specified only full tables
    user_orders = repo.get_all_user_orders_user_only_user_name(
        telegram_id=4104)
    for order, user_name in user_orders:
        print(f'Order: {order.order_id} - {user_name}')
    print('=============')
    for row in user_orders:
        # As you can see, if we specified column instead of full table,
        # we can access it directly from row by using the name of column
        print(f'Order: {row.Order.order_id} - {row.user_name}')
