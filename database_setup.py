# Configuration
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


# Class Code
class Restaurant(Base):
    __tablename__ = 'restaurant'
    
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = True)
    description = Column(String(2500))
    course = Column(String(80))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


# ############ end of file ##########
engine = create_engine(
    'sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)

