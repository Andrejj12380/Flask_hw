import atexit
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

PG_DSN = 'postgresql://app:2461@127.0.0.1:5500/flask_crud'

engine = create_engine(PG_DSN)

Base = declarative_base()


class Owner(Base):
    __tablename__ = 'app_owner'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class Advertisement(Base):
    __tablename__ = 'app_advertisements'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    creation_date = Column(DateTime, server_default=func.now())
    owner_id = Column(Integer, ForeignKey("app_owner.id", ondelete="CASCADE"))
    owner = relationship('Owner', lazy='joined')


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
atexit.register(engine.dispose)
