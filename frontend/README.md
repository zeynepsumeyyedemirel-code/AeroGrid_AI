# AeroGrid AI - Technician Interface

Plain HTML5, CSS and JavaScript (no framework, no build step). Talks to the FastAPI backend through its REST API.

| File | Purpose |
|---|---|
| `index.html` | Semantic page structure, form, result area, connection settings |
| `style.css` | Responsive layout (CSS Grid), light/dark theme, keyboard focus styles |
| `app.js` | `fetch` calls to `/health` and `/query`, timeout handling, demo mode |

## Run locally

1. Start the backend: `docker compose up --build` (API on port 8000).
2. Serve this folder: `cd frontend && python -m http.server 8080`
3. Open http://localhost:8080

## Allow the page to call the API (CORS)

Add to `src/api/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
```

## Demo mode

On `github.io` the page starts in demo mode (no backend needed). Demo answers are placeholders and are labelled as such. Questions outside the demo topics return `INSUFFICIENT_CONTEXT`, mirroring the real guardrail.

## Design notes

- Responsive from phone to desktop; touch targets are at least 48 px for use with gloves or tablets in the field.
- Answers are inserted with `textContent`, never `innerHTML`, so API output cannot inject markup.
- Works offline: system font stack, no external scripts, fonts or CDNs.
- Keyboard: `Ctrl+Enter` submits, visible focus rings, skip link, status changes announced with `aria-live`.
