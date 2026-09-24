import uuid
from typing import Dict, Tuple
from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
from app.games.mooncake.engine import MooncakeEngine

router = APIRouter(prefix="/games/mooncake", tags=["mooncake"])
templates = Jinja2Templates(directory="app/templates")

# In-memory session store mapping session_id -> MooncakeEngine
sessions: Dict[str, MooncakeEngine] = {}


def get_or_create_game(request: Request) -> Tuple[MooncakeEngine, str, bool]:
    """Retrieve existing player game engine or initialize a new session."""
    session_id = request.cookies.get("session_id")
    is_new = False
    if not session_id or session_id not in sessions:
        session_id = uuid.uuid4().hex
        sessions[session_id] = MooncakeEngine()
        is_new = True
    return sessions[session_id], session_id, is_new


def attach_session_cookie(response: Response, session_id: str) -> None:
    response.set_cookie(
        key="session_id",
        value=session_id,
        max_age=30 * 86400,  # 30 days
        httponly=True,
        samesite="lax"
    )


@router.get("")
@router.get("/")
def get_game_page(request: Request):
    game, session_id, is_new = get_or_create_game(request)
    response = templates.TemplateResponse(
        request=request,
        name="games/mooncake.html",
        context={
            "game": game,
            "upgrades": list(game.upgrades.values()),
            "achievements": list(game.achievements.values())
        }
    )
    if is_new:
        attach_session_cookie(response, session_id)
    return response


@router.post("/click")
def handle_click(request: Request):
    game, session_id, is_new = get_or_create_game(request)
    game.click()
    response = templates.TemplateResponse(
        request=request,
        name="games/partials/game_state.html",
        context={
            "game": game,
            "upgrades": list(game.upgrades.values()),
            "achievements": list(game.achievements.values())
        }
    )
    if is_new:
        attach_session_cookie(response, session_id)
    return response


@router.post("/tick")
def handle_tick(request: Request):
    game, session_id, is_new = get_or_create_game(request)
    game.tick(1.0)
    response = templates.TemplateResponse(
        request=request,
        name="games/partials/game_state.html",
        context={
            "game": game,
            "upgrades": list(game.upgrades.values()),
            "achievements": list(game.achievements.values())
        }
    )
    if is_new:
        attach_session_cookie(response, session_id)
    return response


@router.post("/buy/{item_id}")
def handle_buy_upgrade(item_id: str, request: Request):
    game, session_id, is_new = get_or_create_game(request)
    game.buy_upgrade(item_id)
    response = templates.TemplateResponse(
        request=request,
        name="games/partials/game_state.html",
        context={
            "game": game,
            "upgrades": list(game.upgrades.values()),
            "achievements": list(game.achievements.values())
        }
    )
    if is_new:
        attach_session_cookie(response, session_id)
    return response


@router.post("/reset")
def handle_reset(request: Request):
    game, session_id, is_new = get_or_create_game(request)
    game.reset()
    response = templates.TemplateResponse(
        request=request,
        name="games/partials/game_state.html",
        context={
            "game": game,
            "upgrades": list(game.upgrades.values()),
            "achievements": list(game.achievements.values())
        }
    )
    if is_new:
        attach_session_cookie(response, session_id)
    return response
