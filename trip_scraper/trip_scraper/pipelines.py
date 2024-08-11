import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import psycopg2
from psycopg2 import sql
from itemadapter import ItemAdapter

load_dotenv()

def create_database(database_url):
    database_name = database_url.rsplit('/', 1)[-1]
    default_database_url = database_url.rsplit('/', 1)[0] + '/postgres'
    
    conn = psycopg2.connect(default_database_url)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [database_name])
    exists = cur.fetchone()
    if not exists:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))
    
    cur.close()
    conn.close()

DATABASE_URL = os.getenv("DATABASE_URL")

create_database(DATABASE_URL)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String)
    Rating = Column(String)
    Country = Column(String)
    Location = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    Price = Column(String)
    Hotel_img = Column(String)

Base.metadata.create_all(engine)

class HotelscrapPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        hotel = Hotel(
            Title = adapter.get('Title'),
            Rating=adapter.get('Rating'),
            Country = adapter.get('Country'),
            Location=adapter.get('Location'),
            latitude=adapter.get('latitude'),
            longitude=adapter.get('longitude'),
            Price=adapter.get('Price'),
            Hotel_img=adapter.get('Hotel_img')
        )

        session.add(hotel)
        session.commit()
        return item
