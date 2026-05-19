"""
Pydantic models and validation for scraped DC supplier leads.

Every supplier record returned by a skill is validated against the
Supplier schema before being written to disk. Invalid records are
logged and excluded from the final output.
"""

from __future__ import annotations

import json
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


class Supplier(BaseModel):
    """A single data‑center supplier lead."""

    company_name: str = Field(
        ..., min_length=1, description="Official company name"
    )
    website: str = Field(
        ..., min_length=1, description="Homepage URL of the company"
    )
    headquarters: Optional[str] = Field(
        default=None, description="City, State/Country of HQ"
    )
    summary: str = Field(
        ..., min_length=10, description="1–2 sentence description of what they do for data centers"
    )
    categories: List[str] = Field(
        ..., min_length=1, description="Category tags (e.g. EPC, HVAC, UPS …)"
    )
    services: List[str] = Field(
        ..., min_length=1, description="Specific services or products offered"
    )
    retrofit_capable: bool = Field(
        ..., description="Whether they can retrofit / upgrade existing DC facilities"
    )
    notable_clients_or_projects: Optional[List[str]] = Field(
        default=None, description="Named clients or case studies"
    )
    contact_email: Optional[str] = Field(
        default=None, description="Contact email if publicly listed"
    )
    contact_phone: Optional[str] = Field(
        default=None, description="Contact phone if publicly listed"
    )
    source_url: Optional[str] = Field(
        default=None, description="Page URL where the info was found"
    )

    @field_validator("website")
    @classmethod
    def website_must_look_like_url(cls, v: str) -> str:
        v = v.strip()
        if not v.startswith(("http://", "https://")):
            v = "https://" + v
        return v


class SkillResult(BaseModel):
    """The JSON blob a single skill execution returns."""

    skill: str = Field(..., description="Skill identifier, e.g. 'epc_contractors'")
    suppliers: List[Supplier] = Field(
        default_factory=list, description="Supplier leads found by this skill"
    )


class AggregatedReport(BaseModel):
    """Final validated report across all skills."""

    total_leads: int = 0
    skills_run: List[str] = Field(default_factory=list)
    suppliers: List[Supplier] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def validate_skill_result(raw: dict) -> SkillResult:
    """Validate a raw dict against the SkillResult schema.

    Returns a validated SkillResult. Raises pydantic.ValidationError on bad
    data so the caller can handle it gracefully.
    """
    return SkillResult.model_validate(raw)


def validate_supplier(raw: dict) -> Supplier:
    """Validate a single supplier dict."""
    return Supplier.model_validate(raw)


def get_supplier_schema_json() -> str:
    """Return the JSON Schema for SkillResult (for prompt injection)."""
    return json.dumps(SkillResult.model_json_schema(), indent=2)
