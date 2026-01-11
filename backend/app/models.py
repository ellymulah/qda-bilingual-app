from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Language(str, Enum):
    ARABIC = "ar"
    ENGLISH = "en"

class DocumentBase(BaseModel):
    title: str
    language: Language
    content: str
    
class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class AudioAnalysisRequest(BaseModel):
    audio_file_path: str
    language: Language
    template_id: Optional[int] = None

class AudioAnalysisResponse(BaseModel):
    transcript: str
    detected_language: Language
    feedback: str
    sentiment: Optional[str] = None
    key_themes: Optional[List[str]] = None

class Template(BaseModel):
    id: int
    name: str
    description: str
    language: Language
    prompt_template: str
    
    class Config:
        from_attributes = True

class CodeSegment(BaseModel):
    id: int
    document_id: int
    start_position: int
    end_position: int
    code_label: str
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True

class TranslationRequest(BaseModel):
    text: str
    source_language: Language
    target_language: Language

class TranslationResponse(BaseModel):
    translated_text: str
    source_language: Language
    target_language: Language
