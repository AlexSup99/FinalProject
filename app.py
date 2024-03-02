from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from database import SessionLocal
from table_user import User
from table_post import Post
from table_feed import Feed
from schema import UserGet, PostGet, FeedGet



app = FastAPI()


def get_db():
    with SessionLocal() as db:
        return db


@app.get("/user/{id}", response_model=UserGet)
def get_user(id: int, db: Session = Depends(get_db)) -> User:
    result = db.query(User).filter(User.id == id).one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="id not found")
    else:
        return result


@app.get("/post/{id}", response_model=PostGet)
def get_post(id, db: Session = Depends(get_db)):
    result = db.query(Post).filter(Post.id == id).one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="id not found")
    else:
        return result

@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get_user_feed(id: int, limit: int = 10, db: Session = Depends(get_db)):
    feed_actions = db.query(Feed).filter(Feed.user_id == id).order_by(Feed.time.desc()).limit(limit).all()
    if not feed_actions:
        return []
    else:
        return feed_actions

@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get_post_feed(id: int, limit: int = 10, db: Session = Depends(get_db)):
    feed_actions = db.query(Feed).filter(Feed.post_id == id).order_by(Feed.time.desc()).limit(limit).all()
    if not feed_actions:
        return []
    else:
        return feed_actions


@app.get("/post/recommendations/", response_model=List[PostGet])
def get_post_recommendations(limit: int = 10, db: Session = Depends(get_db)):
    top_posts = (
        db.query(Post.id, Post.text, Post.topic)
        .join(Feed, Post.id == Feed.post_id)
        .filter(Feed.action == 'like')
        .group_by(Post.id)
        .order_by(func.count(Feed.post_id).desc())
        .limit(limit)
        .all()
    )
    return top_posts

