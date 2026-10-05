"""RevCRM target class."""

from __future__ import annotations

from hotglue_singer_sdk import typing as th
from hotglue_singer_sdk.target_sdk.target import TargetHotglue

from target_revcrm.sinks import EmailSubscriptionsSink


class TargetRevCRM(TargetHotglue):
    """Target for RevCRM email subscription updates."""

    name = "target-revcrm"
    SINK_TYPES = [EmailSubscriptionsSink]

    config_jsonschema = th.PropertiesList(
        th.Property("client_id", th.StringType, required=True),
        th.Property("client_secret", th.StringType, required=True),
        th.Property("client_code", th.StringType, required=True),
        th.Property(
            "api_url",
            th.StringType,
            default="https://app.roicrm.net/api/1.0",
        ),
        th.Property(
            "token_url",
            th.StringType,
            default="https://roisolutions.us.auth0.com/oauth/token",
        ),
    ).to_dict()


if __name__ == "__main__":
    TargetRevCRM.cli()
