# Session Interface
from sqlalchemy import create_engine
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker


def open_session():
    engine = create_engine('sqlite:///restaurantMenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


def query_all_restaurants():
    session = open_session()
    return session.query(Restaurant).all()


def query_restaurant_by_id(restaurant_id):
    session = open_session()
    return session.query(Restaurant).filter_by(id=restaurant_id).one()


def query_restaurant_by_name(restaurant_name):
    session = open_session()
    return session.query(Restaurant).filter_by(name=restaurant_name).one()


def create_restaurant(restaurant_name=""):
    session = open_session()
    new_restaurant = Restaurant(name=restaurant_name)
    session.add(new_restaurant)
    session.commit()


def edit_restaurant(restaurant_id, restaurant_name=""):
    session = open_session()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if restaurant:
        restaurant.name = restaurant_name
        session.add(restaurant)
        session.commit()


def delete_restaurant(restaurant_id):
    session = open_session()
    print restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    session.delete(restaurant)
    session.commit()
