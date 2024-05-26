from pydantic import BaseModel, Field

from src.utils import types


class ActivityFilter(BaseModel):
    post_url: types.OpStr = Field(None, alias="postUrl")
    type: types.OpStr = Field(None, alias="type")
    video_url: types.OpStr = Field(None, alias="videoUrl")
    img_url: types.OpStr = Field(None, alias="imgUrl")
    post_content: types.OpStr = Field(None, alias="postContent")
    like_count: types.OpInt = Field(None, alias="likeCount")
    comment_count: types.OpInt = Field(None, alias="commentCount")
    repost_count: types.OpInt = Field(None, alias="repostCount")
    post_date: types.OpStr = Field(None, alias="postDate")
    action: types.OpStr = Field(None, alias="action")
    profile_url: types.OpStr = Field(None, alias="profileUrl")
    timestamp: types.OpCoercedDtOrDttm = Field(None, alias="timestamp")
    post_timestamp: types.OpCoercedDtOrDttm = Field(None, alias="postTimestamp")
    agent_id: types.OpStr = Field(None, alias="agentId")
    container_id: types.OpStr = Field(None, alias="containerId")

    class Config:
        orm_mode = True
        json_encoders = {
            types.datetime.datetime: lambda dt: dt.isoformat(),
        }
