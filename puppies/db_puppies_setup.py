# Configuration
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Class Code
class Shelter(Base):
    __tablename__ = 'shelter'
    
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    address = Column(String(120), nullable = False)
    city = Column(String(80), nullable = False)
    state = Column(String(80), nullable = False)
    zipCode = Column(String(80), nullable = False)
    website = Column(String(80), nullable = False)

    def __string__(self):
        return f'<Shelter {self.name}>'


class Puppy(Base):
    __tablename__ = 'puppy'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = True)
    dateOfBirth = Column(Date, nullable = True)
    gender = Column(String(10), nullable = True)
    weight = Column(Float, nullable = True)
    picture = Column(String(300), nullable = True)
    shelter = relationship(Shelter)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))

    def __string__(self):
        return f'<Puppy {self.name}>'


# ############ end of file ##########
engine = create_engine(
    'sqlite:///puppies.db')

Base.metadata.create_all(engine)
