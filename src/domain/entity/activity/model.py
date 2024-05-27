from pydantic import BaseModel, Field, field_validator, AliasChoices
from datetime import datetime
from src.utils import types


class Activity(BaseModel):
    post_url: str = Field(..., validation_alias=AliasChoices("postUrl", "post_url"))
    type: types.OpStr = Field("Unknown", validation_alias=AliasChoices("type"))
    video_url: types.OpStr = Field(None, validation_alias=AliasChoices("videoUrl", "video_url"))
    img_url: types.OpStr = Field(None, validation_alias=AliasChoices("imgUrl", "img_url"))
    post_content: types.OpStr = Field("", validation_alias=AliasChoices("postContent", "post_content"))
    like_count: types.OpInt = Field(0, validation_alias=AliasChoices("likeCount", "like_count"))
    comment_count: types.OpInt = Field(0, validation_alias=AliasChoices("commentCount", "comment_count"))
    repost_count: types.OpInt = Field(0, validation_alias=AliasChoices("repostCount", "repost_count"))
    post_date: types.OpStr = Field(None, validation_alias=AliasChoices("postDate", "post_date"))
    action: types.OpStr = Field("Unknown", validation_alias=AliasChoices("action"))
    profile_url: str = Field(..., validation_alias=AliasChoices("profileUrl", "profile_url"))
    timestamp: datetime = Field(..., validation_alias=AliasChoices("timestamp"))
    post_timestamp: datetime = Field(..., validation_alias=AliasChoices("postTimestamp", "post_timestamp"))
    agent_id: types.OpStr = Field(None, validation_alias=AliasChoices("agentId", "agent_id"))
    container_id: types.OpStr = Field(None, validation_alias=AliasChoices("containerId", "container_id"))

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_alias = True
        populate_by_field_name = True
        json_encoders = {
            types.datetime.datetime: lambda dt: dt.replace(tzinfo=None),
        }

    @field_validator("timestamp", "post_timestamp", mode='after')
    def remove_offset(cls, value: datetime) -> datetime:
        return value.replace(tzinfo=None)

