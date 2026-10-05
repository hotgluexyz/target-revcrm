"""RevCRM sinks."""

from __future__ import annotations

from typing import Any

from target_revcrm.client import RevCRMRecordSink


class EmailSubscriptionsSink(RevCRMRecordSink):
    """Marks a matching RevCRM donor email as unsubscribed."""

    name = "email_subscriptions"
    endpoint = "/donors/"

    def preprocess_record(self, record: dict[str, Any], _context: dict) -> dict[str, Any]:
        """Keep the ETL's normalized unsubscribe record unchanged."""
        return record

    def upsert_record(
        self,
        record: dict[str, Any],
        _context: dict,
    ) -> tuple[str, bool, dict[str, Any]]:
        """Look up a donor email and set its contact status to not contactable."""
        email = record["email"]
        donor_response = self.request_api(
            "GET",
            endpoint=self.endpoint,
            params={"email": email, "include": "emails", "limit": 1},
        )
        donors = donor_response.json().get("items", [])
        for donor in donors:
            for donor_email in donor.get("email_addresses", []):
                if donor_email.get("email_address", "").lower() == email.lower():
                    response = self.request_api(
                        "PATCH",
                        endpoint=(
                            f"/donors/{donor['roi_family_id']}/emails/{donor_email['email_id']}/"
                        ),
                        request_data={"contact_status": "N"},
                    )
                    return donor_email["email_id"], response.ok, {}

        message = f"No RevCRM donor email matches {email!r}."
        raise ValueError(message)
