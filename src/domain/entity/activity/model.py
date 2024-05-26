from pydantic import BaseModel, Field

from src.utils import types


class Activity(BaseModel):
    post_url: str = Field(..., alias="postUrl")
    type: types.OpStr = Field("Unknown", alias="type")
    video_url: types.OpStr = Field(None, alias="videoUrl")
    img_url: types.OpStr = Field(None, alias="imgUrl")
    post_content: types.OpStr = Field("", alias="postContent")
    like_count: types.OpInt = Field(0, alias="likeCount")
    comment_count: types.OpInt = Field(0, alias="commentCount")
    repost_count: types.OpInt = Field(0, alias="repostCount")
    post_date: types.OpStr = Field(None, alias="postDate")
    action: types.OpStr = Field("Unknown", alias="action")
    profile_url: str = Field(..., alias="profileUrl")
    timestamp: types.CoercedDtOrDttm = Field(..., alias="timestamp")
    post_timestamp: types.CoercedDtOrDttm = Field(..., alias="postTimestamp")
    agent_id: types.OpStr = Field(None, alias="agentId")
    container_id: types.OpStr = Field(None, alias="containerId")

    class Config:
        orm_mode = True
        json_encoders = {
            types.datetime.datetime: lambda dt: dt.isoformat(),
        }
