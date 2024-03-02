from database import Base, SessionLocal
from sqlalchemy import  Column, Integer, String, func, desc

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, name = 'id')
    gender = Column(Integer, name = 'gender')
    age = Column(Integer, name = 'age')
    country = Column(String, name = 'country')
    city = Column(String, name = 'city')
    exp_group = Column(Integer, name = 'exp_group')
    os = Column(String, name = 'os')
    source = Column(String, name = 'source')


if __name__ == "__main__":
    session = SessionLocal()

    result = (
        session.query(User.country, User.os, func.count())
        .filter(User.exp_group == 3)
        .group_by(User.country, User.os)
        .having(func.count() > 100)
        .order_by(desc(func.count()))
        .all()
    )

    result = [(country, os, count) for country, os, count in result]

    print(result)
