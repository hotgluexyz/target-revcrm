"""HTTP client and sink base classes for RevCRM."""

from __future__ import annotations

import requests
from hotglue_singer_sdk.target_sdk.client import HotglueBaseSink, HotglueSink


class RevCRMSink(HotglueBaseSink):
    """Base sink with RevCRM client-credentials authentication."""

    @property
    def base_url(self) -> str:
        """Return the configured RevCRM API root."""
        return self.config["api_url"].rstrip("/")

    @property
    def http_headers(self) -> dict[str, str]:
        """Build RevCRM API headers with a cached access token."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "ROI-CLIENT-CODE": self.config["client_code"],
        }

    @property
    def access_token(self) -> str:
        """Obtain and cache a RevCRM Auth0 access token for this process."""
        if not hasattr(self, "_access_token"):
            response = requests.post(
                self.config["token_url"],
                json={
                    "client_id": self.config["client_id"],
                    "client_secret": self.config["client_secret"],
                    "audience": "https://app.roicrm.net/api/1.0/",
                    "grant_type": "client_credentials",
                    "roi_client_code": self.config["client_code"],
                },
                timeout=30,
            )
            response.raise_for_status()
            self._access_token = response.json()["access_token"]
        return self._access_token


class RevCRMRecordSink(RevCRMSink, HotglueSink):
    """Base class for record-at-a-time RevCRM sinks."""
