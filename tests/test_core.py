"""Tests for RevCRM email subscription updates."""

from unittest.mock import Mock, call

import pytest

from target_revcrm.sinks import EmailSubscriptionsSink


def email_subscriptions_sink() -> EmailSubscriptionsSink:
    """Return a sink with non-secret test configuration."""
    sink = object.__new__(EmailSubscriptionsSink)
    sink._config = {  # noqa: SLF001
        "api_url": "https://app.roicrm.net/api/1.0",
        "client_id": "client-id",
        "client_secret": "client-secret",
        "client_code": "DEMO2",
        "token_url": "https://roisolutions.us.auth0.com/oauth/token",
    }
    return sink


def test_email_subscription_marks_matching_revcrm_email_unsubscribed() -> None:
    """The target finds the matching nested donor email before patching it."""
    sink = email_subscriptions_sink()
    donors_response = Mock()
    donors_response.json.return_value = {
        "items": [
            {
                "roi_family_id": "12",
                "email_addresses": [{"email_id": "34", "email_address": "ada@example.org"}],
            }
        ]
    }
    patch_response = Mock(ok=True)
    sink.request_api = Mock(side_effect=[donors_response, patch_response])

    result = sink.upsert_record({"email": "Ada@Example.org"}, {})

    assert result == ("34", True, {})
    assert sink.request_api.call_args_list == [
        call(
            "GET",
            endpoint="/donors/",
            params={"email": "Ada@Example.org", "include": "emails", "limit": 1},
        ),
        call(
            "PATCH",
            endpoint="/donors/12/emails/34/",
            request_data={"contact_status": "N"},
        ),
    ]


def test_email_subscription_fails_when_no_revcrm_email_matches() -> None:
    """An unresolved ActiveCampaign email fails instead of modifying another donor."""
    sink = email_subscriptions_sink()
    donors_response = Mock()
    donors_response.json.return_value = {"items": []}
    sink.request_api = Mock(return_value=donors_response)

    with pytest.raises(ValueError, match="No RevCRM donor email"):
        sink.upsert_record({"email": "missing@example.org"}, {})
