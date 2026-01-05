```markdown
# copilot-instructions.md

## project goal

Build a small but real FastAPI service that presents a “REST meets self-introduction” API. The primary deliverable is a polished OpenAPI experience at `/docs` (Swagger UI) plus a working API behind it. The demo should feel playful but still engineered: clean models, consistent responses, good examples, sensible HTTP semantics, and a couple of intentional Easter eggs.

## non-goals

- No database required for v1; use in-memory or file-based sample data.
- No auth required for v1 (unless added as an optional stretch).
- No external dependencies that complicate local demo runs; keep it lightweight.

## stack

- Python 3.11+ (prefer 3.12 if available)
- FastAPI
- Uvicorn
- Pydantic v2
- Pytest (for a small test set)
- Optional: ruff + black (if already in the repo; otherwise keep code style clean without adding tools)

## required endpoints (v1)

Implement the following endpoints. Ensure they show up nicely categorized in Swagger tags.

### profile
- `GET /profile`
  - Returns the main profile object.
  - Supports query params:
    - `mode` with allowed values: `default`, `conference`, `afterhours`
    - `unlock` optional; if `unlock=ff69b4`, include additional fields in the response (Easter egg).

- `GET /profile/quote`
  - Query param `topic` optional; return a quote object; if unknown topic, return a default “it depends”-style quote.

### skills
- `GET /skills`
  - Optional filter: `domain` (string)
  - Returns list of skills with id, name, level, tags, and example use cases.


### talks
- `GET /talks`
  - Optional filter: `year` (int)
  - Return list; include pagination fields even if static (`page`, `page_size`, `total`).


### projects
- `GET /projects`

  - Return a structured object describing components and integrations



## response design rules

- Use Pydantic models for all responses and requests; no untyped dicts in route handlers.
- Always return JSON with consistent error shape:
  - `{ "error": { "code": "...", "message": "...", "details": {...} } }`
- 404 responses must include the same error shape with `code="not_found"`.
- 422 validation errors can be left as FastAPI defaults unless easily wrapped.

## openapi and swagger requirements

- The OpenAPI docs must look “fancy” by default:
  - Set API title, description, and version.
  - NEVER use emojis in titles or descriptions.
  - Use tags with descriptions (Profile, Skills, Talks, Projects, Status, Easter Eggs).
  - Provide examples for at least:
    - `/profile` response
    - one `Skill` response
    - one `Talk` response
    - the 418 error payload
- Customize Swagger UI:
  - Provide a custom CSS file (pink accents, subtle punk vibe; keep it tasteful).
  - Ensure `/docs` uses that CSS.
  - If feasible, add a small custom topbar title.

Implementation hint: serve static files via FastAPI and configure Swagger UI parameters. Keep the customization self-contained in `app/main.py` and `app/static/`.

## data handling

- Seed data lives in `app/data/` as JSON or Python constants.
- Provide stable ids for skills, talks, and projects.
- Keep data small but realistic: 5–8 skills, 3–6 talks, 3–5 projects.

## project structure

Use this structure (create folders if missing):

- `app/`
  - `main.py` (FastAPI app, routes included or router wiring)
  - `api/`
    - `routers/` (one router per domain: profile, skills, talks, projects, status, easter_eggs)
  - `models/` (Pydantic request/response models)
  - `services/` (business logic, rate limiting, data access)
  - `data/` (seed data files)
  - `static/` (swagger CSS; optional logo)
- `tests/`
  - `test_profile.py`, `test_easter_eggs.py` at minimum

## coding style and quality

- Prefer small route handlers; put logic into `services/`.
- Add type hints everywhere.
- Keep functions pure where possible; side effects limited to in-memory stores.
- Use `APIRouter` with prefixes and tags.
- Use `HTTPException` only at the boundary; prefer a helper to build consistent error responses.

## tests (minimum)

Write pytest tests using FastAPI TestClient:

- `/profile` returns 200 and matches expected keys


## run instructions

Ensure `README.md` includes:

- create venv
- install requirements
- run with uvicorn
- open docs at `http://127.0.0.1:8000/docs`
- a couple of curl examples, including the unlock parameter

## tone and content guidance

- Keep the API content playful but not chaotic; jokes should not break schemas.
- Use inclusive, neutral phrasing; do not invent personal facts beyond what is provided in the seed data.
- Avoid slang that could age poorly; keep it witty and crisp.

## implementation checklist

Copilot should help implement:

- app skeleton with routers and models
- seed data + service layer
- swagger UI customization via static CSS
- OpenAPI metadata and examples
- basic tests
- consistent error payload helper

If something is ambiguous, choose the simplest implementation that makes the Swagger experience impressive and the demo reliable.
```
