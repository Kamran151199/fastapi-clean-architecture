"""
This module contains the ORM (SQLAlchemy) models for the activity table in Postgres.
"""

from sqlalchemy import Column, Integer, String, DateTime

from src.infrastructure.db.postgres.orm.base import Base


class Activity(Base):
    """
    ORM model for the activity table.
    """

    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    post_url = Column(String, nullable=False)
    type = Column(String, nullable=False)
    video_url = Column(String, nullable=True)
    img_url = Column(String, nullable=True)
    post_content = Column(String, nullable=False)
    like_count = Column(Integer, nullable=False)
    comment_count = Column(Integer, nullable=False)
    repost_count = Column(Integer, nullable=False)
    post_date = Column(String, nullable=True)
    action = Column(String, nullable=False)
    profile_url = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    post_timestamp = Column(DateTime, nullable=False)
    agent_id = Column(String, nullable=False)
    container_id = Column(String, nullable=False)

    def __repr__(self):
        return (
            f"<Activity(post_url={self.post_url}, type={self.type}, video_url={self.video_url}, "
            f"img_url={self.img_url}, post_content={self.post_content}, like_count={self.like_count}, "
            f"comment_count={self.comment_count}, repost_count={self.repost_count}, post_date={self.post_date}, "
            f"action={self.action}, profile_url={self.profile_url}, timestamp={self.timestamp}, "
            f"post_timestamp={self.post_timestamp}) agent_id={self.agent_id}, container_id={self.container_id}>"
        )
