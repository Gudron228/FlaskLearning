from sqlalchemy import create_engine, MetaData, Table, String, Integer, Boolean, DateTime, Text, Column
from datetime import datetime

metadata = MetaData()

engine = create_engine("mysql+pymysql://root:vovik2003@localhost/test")

conn = engine.connect()
mainmenu = Table('mainmenu', metadata,
                 Column('id', Integer(), primary_key=True, autoincrement=True),
                 Column('title', Text(), nullable=False),
                 Column('url', Text(), nullable=False))
metadata.create_all(engine)
conn.commit()
conn.close()

conn = engine.connect()
posts = Table('posts1', metadata,
              Column('id', Integer(), primary_key=True, autoincrement=True),
              Column('title', Text(), nullable=False),
              Column('text', Text(), nullable=False),
              Column('time', DateTime(), default=datetime.now))
metadata.create_all(engine)
conn.commit()
conn.close()
