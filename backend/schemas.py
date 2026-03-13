from pydantic import BaseModel

class TextInput(BaseModel):
    user_id: str
    text: str
