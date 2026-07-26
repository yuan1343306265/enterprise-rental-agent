from datetime import datetime
from pydantic import BaseModel,ConfigDict

class ConversationMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role:str
    content:str
    created_at:datetime

class SessionHistoryResponse(BaseModel):
    session_id:str
    messages:list[ConversationMessageResponse]