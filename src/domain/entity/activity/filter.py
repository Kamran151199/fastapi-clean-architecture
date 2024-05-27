from pydantic import BaseModel, Field, AliasChoices

from src.utils import types


class ActivityFilter(BaseModel):
    post_url: types.OpStr = Field(None, validation_alias=AliasChoices("postUrl", "post_url"))
    type: types.OpStr = Field(None, validation_alias=AliasChoices("type"))
    video_url: types.OpStr = Field(None, validation_alias=AliasChoices("videoUrl", "video_url"))
    img_url: types.OpStr = Field(None, validation_alias=AliasChoices("imgUrl", "img_url"))
    post_content: types.OpStr = Field(None, validation_alias=AliasChoices("postContent", "post_content"))
    like_count: types.OpInt = Field(None, validation_alias=AliasChoices("likeCount", "like_count"))
    comment_count: types.OpInt = Field(None, validation_alias=AliasChoices("commentCount", "comment_count"))
    repost_count: types.OpInt = Field(None, validation_alias=AliasChoices("repostCount", "repost_count"))
    post_date: types.OpStr = Field(None, validation_alias=AliasChoices("postDate", "post_date"))
    action: types.OpStr = Field(None, validation_alias=AliasChoices("action"))
    profile_url: types.OpStr = Field(None, validation_alias=AliasChoices("profileUrl", "profile_url"))
    timestamp: types.OpCoercedDtOrDttm = Field(None, validation_alias=AliasChoices("timestamp"))
    post_timestamp: types.OpCoercedDtOrDttm = Field(None, validation_alias=AliasChoices("postTimestamp", "post_timestamp"))
    agent_id: types.OpStr = Field(None, validation_alias=AliasChoices("agentId"))
    container_id: types.OpStr = Field(None, validation_alias=AliasChoices("containerId"))

    class Config:
        orm_mode = True
        json_encoders = {
            types.datetime.datetime: lambda dt: dt.isoformat(),
        }
