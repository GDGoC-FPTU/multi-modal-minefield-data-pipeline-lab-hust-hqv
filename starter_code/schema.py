from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================
# Your task is to define the Unified Schema for all sources.
# This is v1. Note: A breaking change is coming at 11:00 AM!

class UnifiedDocument(BaseModel):
    """Unified schema for all data sources in the minefield pipeline."""

    document_id: str = Field(..., description="Unique identifier for the document")
    content: str = Field(..., description="Main content/text of the document")
    source_type: str = Field(..., description="Source type: PDF, CSV, HTML, Transcript, Code")
    author: Optional[str] = Field(default="Unknown", description="Author or creator of the document")
    timestamp: Optional[datetime] = Field(default=None, description="When the document was created/modified")

    # Source-specific metadata
    source_metadata: dict = Field(default_factory=dict, description="Source-specific fields")

    # Quality and processing metadata
    quality_score: Optional[float] = Field(default=None, description="Quality score (0-1) from QA checks")
    is_valid: bool = Field(default=True, description="Whether document passed QA validation")
    validation_errors: List[str] = Field(default_factory=list, description="List of validation errors if any")

    # Processing tracking
    processed_at: Optional[datetime] = Field(default=None, description="When document was processed")
    processing_version: str = Field(default="v1", description="Schema version used for processing")

    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "doc_001",
                "content": "Sample content here",
                "source_type": "PDF",
                "author": "John Doe",
                "timestamp": "2026-04-24T12:00:00",
                "source_metadata": {"page_count": 10, "file_name": "lecture.pdf"},
                "quality_score": 0.95,
                "is_valid": True,
                "validation_errors": [],
                "processed_at": "2026-04-24T12:15:00",
                "processing_version": "v1"
            }
        }
