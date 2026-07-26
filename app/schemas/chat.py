from pydantic import BaseModel,Field

class ChatRequest(BaseModel):
    message: str= Field(min_length=1,max_length=1000)
    session_id: str = Field(
        default="default",
        min_length=1,
        max_length=1000,
    )

class ChatResponse(BaseModel):
    success:bool
    reply : str
    session_id:str
    