from __future__ import annotations

from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.modules.organizations.schemas import (
    OrganizationCreate,
    OrganizationListResponse,
    OrganizationSummary,
)
from app.shared.responses.pagination import PaginationMeta


def test_organization_create_accepts_valid_payload() -> None:
    payload = OrganizationCreate(
        name="Decision IQ",
        slug="decision-iq",
        email="team@decisioniq.example",
        website="https://decisioniq.example",
        owner_id=uuid4(),
    )

    assert payload.name == "Decision IQ"
    assert str(payload.website) == "https://decisioniq.example/"
    assert payload.email == "team@decisioniq.example"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("email", "not-an-email"),
        ("website", "example.com"),
        ("slug", "Invalid Slug"),
        ("name", ""),
    ],
)
def test_organization_create_validates_core_fields(field: str, value: str) -> None:
    base_payload = {
        "name": "Decision IQ",
        "slug": "decision-iq",
        "email": "team@decisioniq.example",
        "website": "https://decisioniq.example",
        "owner_id": uuid4(),
    }
    base_payload[field] = value

    with pytest.raises(ValidationError):
        OrganizationCreate(**base_payload)


def test_organization_list_response_wraps_summaries() -> None:
    summary = OrganizationSummary(
        id=uuid4(),
        name="Decision IQ",
        slug="decision-iq",
        description="Workspace for analytics",
        status="active",
        created_at="2026-07-11T00:00:00Z",
    )

    response = OrganizationListResponse(
        data=[summary],
        meta=PaginationMeta(page=1, page_size=20, total_items=1, total_pages=1),
    )

    assert response.data[0].slug == "decision-iq"
