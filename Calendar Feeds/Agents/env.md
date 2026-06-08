# ENV — Notion Database IDs

All IDs are dash-formatted UUIDs. Reference this file whenever a Notion API call is needed.

---

## Workspace Token
ntn_z87966143341wFDpXUisYGSE1LQMxiVuwv2WWZgnJ3q3LR

---

## Dashboard Page

| Database | ID |
|---|---|
| About Me | 36520c51-aebe-80ac-8ce6-cd30b4e6aa9c |
| State (Entries) | 36420c51-aebe-80b5-ba08-f6a5c28b1987 |
| Contacts | 36420c51-aebe-80ca-bdbe-d632050b2e34 |
| Preferences | 36420c51-aebe-8094-9bab-ddbe11d22c94 |
| Time Block | 36820c51-aebe-804d-a724-dcea15e9719c |
| Constraints | 36520c51-aebe-80bd-8f09-da0d11785980 |

---

## Projects & Tasks Page

| Database | ID |
|---|---|
| Projects | 36520c51-aebe-80be-aecd-c13b87fd9551 |
| Other | 29820c51-aebe-80b4-abc4-c5147ddc288d |
| Task Dump | 36720c51-aebe-80b1-ad44-e467aa4ed574 |

---

## Project Internal Task Databases

| Project | Tasks DB ID |
|---|---|
| HVR Outreaching Phase | 36720c51-aebe-80cd-9e0a-da37092b2121 |
| MVS Studios / Jarwix Notion Rework | 36720c51-aebe-80c4-b53d-f1ec14e9210a |
| AE Loader | 36720c51-aebe-80d9-bdfb-caf746f3e9ad |
| Finish Reading 3 Books | 36520c51-aebe-8170-9dbb-ce76641b1e52 |

> ⚠️ Internal Tasks database IDs are not discoverable via search. Always call `API-get-block-children` on the project page ID to surface them, then retrieve the schema via `API-retrieve-a-database` before writing.

---

## Calendar Feeds Page

| Database | ID |
|---|---|
| Feed | 29520c51-aebe-8079-8d10-db123c986db0 |
| Changes | 36520c51-aebe-805b-a2e0-ff68924d7029 |

---

## Critical API Quirks

- **Feed title property key has a leading space**: `' Calendar'` — not `'Calendar'`. Using the unspaced version causes creation failures.
- `Done?` property uses `select` type. Default on creation: `'Skipped'`.
- `API-query-data-source` with `sorts` parameters is unreliable — query with `page_size` only, or fall back to `API-post-search` with `filter: {'property': 'object', 'value': 'page'}`.
- Time blocks use ISO 8601 format with explicit PT offset: `-07:00`.
- To trash an incorrectly created page: `API-patch-page` with `in_trash: true`.
