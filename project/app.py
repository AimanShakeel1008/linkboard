#!/usr/bin/env python3
"""
app.py — LinkBoard v1, now a real API built on a real framework (FastAPI).

WHERE WE CAME FROM:
    Phases 2-3 built an HTTP server BY HAND from raw sockets — parsing request
    lines, assembling responses, routing with a giant if/elif. That was the point:
    to prove nothing about the web is magic. But hand-writing every route, parsing
    every body, and formatting every response is exhausting and error-prone. Now
    that we KNOW what a framework does, we let one do it for us.

WHAT A FRAMEWORK DOES (all the stuff we did by hand, now automatic):
    * Routing — map "POST /links" to a function, by decorator, no if/elif tree.
    * Parsing — read the request body and turn JSON into typed Python objects.
    * Validation — reject a request with a missing/bad field BEFORE our code runs.
    * Serialization — turn our returned Python object into a JSON response.
    * Status codes, headers, errors — sensible defaults, easily overridden.
    We wrote each of those from scratch, so none of it is a black box now — you'll
    recognise every step the framework is quietly performing.

THIS IS A REST API:
    LinkBoard is now organised around RESOURCES (things: links, comments) that you
    act on with HTTP METHODS (verbs: GET to read, POST to create). "GET /links"
    = list the links; "POST /links" = create a link; "POST /links/3/upvote" =
    act on link 3. That noun-and-verb style is REST, and it's Part C-D of the
    lesson made real.

THE DELIBERATE FLAW (again, on purpose):
    Data lives in a JSON file via storage.py, whose upvote is a read-modify-write
    with no locking. Run race_demo.py and watch two simultaneous upvotes eat a
    vote. That lost vote is the reason Phase 6 exists.

Run it (from WSL, after installing deps — see project/README.md):
    cd /mnt/d/Projects/linkboard/project
    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn app:app --reload --port 8000
Then open http://localhost:8000/docs for the auto-generated API explorer.
"""

import time
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

import storage


def log(tag: str, message: str) -> None:
    """Narrated, flushed logging — identical style to server.py and storage.py."""
    now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{now} [{tag}] {message}", flush=True)


# ===========================================================================
# THE APP OBJECT
# `app` is the whole application. The metadata below shows up on the automatic
# docs page at /docs — one of the biggest quality-of-life wins of a framework:
# an interactive API explorer you never had to build.
# ===========================================================================

app = FastAPI(
    title="LinkBoard API",
    version="1.0",
    description="A Hacker News-style link board — Phase 4, a JSON REST API.",
)


# ===========================================================================
# REQUEST-JOURNEY LOGGING (middleware)
# A "middleware" runs on EVERY request, before and after our route function —
# the framework's version of the [REQUEST]/[SEND] lines we hand-wrote in the
# socket server. Here we log the incoming request and the outgoing status + time,
# so you can still watch each request flow through the system.
# ===========================================================================

@app.middleware("http")
async def journey_logger(request: Request, call_next):
    start = time.perf_counter()
    log("REQUEST", f"{request.method} {request.url.path} — handling")
    response = await call_next(request)         # run the matching route function
    ms = (time.perf_counter() - start) * 1000
    log("RESPONSE", f"{request.method} {request.url.path} -> "
                    f"{response.status_code} in {ms:.1f}ms")
    return response


# ===========================================================================
# SCHEMAS (Pydantic models)
# These classes describe the SHAPE of request bodies. FastAPI uses them to:
#   * parse incoming JSON into a typed object,
#   * VALIDATE it (a missing 'title' or a non-string 'url' is auto-rejected with
#     a 422 before our code runs — we never write that check ourselves),
#   * document it on the /docs page.
# This is validation-by-declaration: you say what you WANT, not how to check it.
# ===========================================================================

class LinkIn(BaseModel):
    """The body a client sends to submit a new link."""
    title: str = Field(min_length=1, max_length=200, examples=["A great article"])
    url: str = Field(min_length=1, examples=["https://example.com"])


class CommentIn(BaseModel):
    """The body a client sends to add a comment."""
    author: str = Field(min_length=1, max_length=80, examples=["ada"])
    text: str = Field(min_length=1, max_length=1000, examples=["Loved this!"])


# ===========================================================================
# ROUTES — the API's resources and the verbs that act on them.
#
# Each decorator (@app.get, @app.post) is the framework doing the routing we used
# to do by hand. The function name doesn't matter; the decorator's method + path
# do. Whatever we RETURN, FastAPI serializes to JSON automatically.
# ===========================================================================

@app.get("/")
def root():
    """A friendly welcome + a map of the API, returned as JSON."""
    log("API", "/ welcome")
    return {
        "app": "LinkBoard API v1",
        "try": {
            "interactive_docs": "GET /docs",
            "list_links": "GET /links",
            "one_link": "GET /links/{id}",
            "submit_link": "POST /links   body: {title, url}",
            "upvote": "POST /links/{id}/upvote",
            "comment": "POST /links/{id}/comments   body: {author, text}",
        },
        "note": "Data is a JSON file. Run race_demo.py to watch two upvotes "
                "collide — the reason Phase 6 brings a real database.",
    }


@app.get("/links")
def list_links():
    """List all links, most-upvoted first. This is a READ, so it's a GET."""
    links = storage.list_links()
    log("API", f"GET /links -> returning {len(links)} links")
    return {"count": len(links), "links": links}


@app.get("/links/{link_id}")
def get_link(link_id: int):
    """Fetch a single link by id. FastAPI reads {link_id} from the path AND
    converts it to an int for us (a non-numeric id auto-404s with a clear error).
    A missing link is a real 404 — raised, not hand-assembled."""
    link = storage.get_link(link_id)
    if link is None:
        log("API", f"GET /links/{link_id} -> not found -> 404")
        raise HTTPException(status_code=404, detail=f"No link with id {link_id}")
    log("API", f"GET /links/{link_id} -> found '{link['title']}'")
    return link


@app.post("/links", status_code=201)
def submit_link(payload: LinkIn):
    """Create a new link. Because the parameter is typed as LinkIn, FastAPI has
    ALREADY parsed the JSON body and validated it by the time we run — `payload`
    is a clean, guaranteed-valid object. We return 201 Created (Phase 3's honest
    status for 'a new thing was made')."""
    link = storage.add_link(payload.title, payload.url)
    log("API", f"POST /links created id={link['id']} '{link['title']}' -> 201")
    return link


@app.post("/links/{link_id}/upvote")
def upvote_link(link_id: int):
    """Add one point to a link — the RACE-PRONE endpoint.

    It's a plain `def` (not `async def`) on purpose: FastAPI runs sync endpoints
    in a THREAD POOL, so two upvotes really can run at the SAME TIME on different
    threads. That real concurrency, plus storage.py's unlocked read-modify-write,
    is what lets race_demo.py reliably make a vote disappear. An async endpoint
    would quietly serialize on the event loop and hide the bug — which is its own
    lesson about how easy races are to miss."""
    link = storage.upvote_link(link_id)
    if link is None:
        log("API", f"POST /links/{link_id}/upvote -> not found -> 404")
        raise HTTPException(status_code=404, detail=f"No link with id {link_id}")
    log("API", f"POST /links/{link_id}/upvote -> points now {link['points']}")
    return link


@app.post("/links/{link_id}/comments", status_code=201)
def add_comment(link_id: int, payload: CommentIn):
    """Attach a comment to a link. Note the nested resource in the path:
    a comment belongs to a link, so it lives UNDER that link — /links/3/comments.
    That containment is a core REST design idea (lesson Part C)."""
    link = storage.add_comment(link_id, payload.author, payload.text)
    if link is None:
        log("API", f"POST /links/{link_id}/comments -> not found -> 404")
        raise HTTPException(status_code=404, detail=f"No link with id {link_id}")
    log("API", f"POST /links/{link_id}/comments by {payload.author!r} -> 201")
    return link


# Running `python3 app.py` directly is handy, but the normal way to run a FastAPI
# app is with the `uvicorn` server (see the docstring / README) so you get the
# auto-reload-on-save and proper production-style serving.
if __name__ == "__main__":
    import uvicorn
    log("BOOT", "starting LinkBoard API via uvicorn on http://localhost:8000")
    log("BOOT", "open http://localhost:8000/docs for the interactive explorer")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
