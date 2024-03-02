from database import Base, SessionLocal
from sqlalchemy import  Column, Integer, String, desc


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key = True, name = 'id')
    text = Column(String, name = 'text')
    topic = Column(String, name = 'topic')


if __name__ == '__main__':
    temp = []
    session = SessionLocal()
    result = (
        session.query(Post).filter(Post.topic == 'business').order_by(desc(Post.id)).limit(10)
    )
    for x in result:
        temp.append(x.id)