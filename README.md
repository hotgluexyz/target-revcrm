# target-revcrm

`target-revcrm` is a Singer target for **RevCRM**, built with the [Hotglue Singer SDK](https://github.com/hotgluexyz/HotglueSingerSDK) (`TargetHotglue`, HTTP sinks, SDK authenticators).

This project was generated from the Hotglue target cookiecutter with:

| Option | Value |
|--------|--------|
| `auth_method` | `Bearer Token` |
| `sinks` | `EmailSubscriptions | record` |
| `base_url` | `https://app.roicrm.net/api/1.0` |

## Project layout

| Path | Role |
|------|------|
| `target_revcrm/target.py` | `TargetRevCRM` — config schema, `SINK_TYPES`, optional `default_sink_class` and `access_token_support` |
| `target_revcrm/client.py` | `RevCRMSink` base class, `RecordSink` / `BatchSink` stubs, `authenticator` |
| `target_revcrm/sinks.py` | Per-stream sink classes (`FallbackSink` or named `*Sink` classes) |
| `target_revcrm/auth.py` | Present only when generated with **OAuth2** (removed by cookiecutter hook otherwise) |
| `.secrets/config.json` | Sample config matching your `auth_method` |

## Configuration

Settings are defined in `config_jsonschema` on `TargetRevCRM` in `target_revcrm/target.py`.
For this project (**Bearer Token**), config includes: `access_key` (bearer token).

Inspect the live schema:

```bash
target-revcrm --about
target-revcrm --about --format=markdown
```

Local secrets: edit `.secrets/config.json` (shape matches `auth_method` above).

## Authentication

| `auth_method` | Implementation |
|---------------|----------------|
| **OAuth2** | `RevCRMAuthenticator` in `auth.py`; `TargetRevCRM.access_token_support()` returns the authenticator class and token URL (replace the TODO endpoint in `target.py`). |
| **Bearer Token** | `BearerTokenAuthenticator` in `client.py` |
| **Basic Auth** | `BasicAuthenticator` with `username` / `password` |
| **API Key** | `ApiAuthenticator` with configurable header name/prefix |

HTTP calls use `base_url` on `RevCRMSink` (`https://app.roicrm.net/api/1.0` unless you change it in `client.py`).

## Sinks

Sinks are declared at scaffold time as `StreamName | record` or `StreamName | batch`, comma-separated.

Generated with: `EmailSubscriptions | record`
**Named sinks:** `sinks.py` defines one class per stream; `target.py` registers them in `SINK_TYPES`. Implement `endpoint` (and request logic) per sink in `sinks.py` / overrides on `client.py` bases.

Shared HTTP behavior lives in `client.py` (`RevCRMRecordSink` / `RevCRMBatchSink` as generated).

## Usage

```bash
target-revcrm --version
target-revcrm --help
tap-smoke-test | target-revcrm --config /path/to/config.json
```

## Developer setup

Prerequisites: Python 3.10+, [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pytest
uv run target-revcrm --help
tox -e lint    # ruff check + format
```

For implementation notes and conventions, see `AGENTS.md` (or `CLAUDE.md` if that was selected at generation).

## References

- [Hotglue Singer SDK](https://github.com/hotgluexyz/HotglueSingerSDK)
