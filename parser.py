from pydantic import BaseModel

class PostAnalysis(BaseModel):
    
    tone: str
    intent: str
    communication_style: str
    summary: str
