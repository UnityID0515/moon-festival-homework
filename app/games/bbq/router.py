import uuid
from typing import Dict, Tuple
from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
from app.games.bbq.engine import BBQEngine, FOOD_DEFINITIONS

router = APIRouter(prefix="/games/bbq", tags=["bbq"])
templates = Jinja2Templates(directory="app/templates")

# Session store mapping session_id -> BBQEngine
bbq_sessions: Dict[str, BBQEngine] = {}


def get_or_create_bbq(request: Request) -> Tuple[BBQEngine, str, bool]:
    session_id = request.cookies.get("session_id")
    is_new = False
    if not session_id or session_id not in bbq_sessions:
        if not session_id:
            session_id = uuid.uuid4().hex
            is_new = True
        bbq_sessions[session_id] = BBQEngine()
    return bbq_sessions[session_id], session_id, is_new


def attach_session_cookie(response: Response, session_id: str) -> None:
    response.set_cookie(
        key="session_id",
        value=session_id,
        max_age=30 * 86400,
        httponly=True,
        samesite="lax"
    )


def render_bbq_state(request: Request, engine: BBQEngine, session_id: str, is_new: bool, template_name: str = "games/partials/bbq_state.html"):
    response = templates.TemplateResponse(
        request=request,
        name=template_name,
        context={
            "engine": engine,
            "foods": list(FOOD_DEFINITIONS.values()),
            "slots": engine.slots,
            "any_cooking": any(s is not None for s in engine.slots)
        }
    )
    if is_new:
        attach_session_cookie(response, session_id)
    return response


@router.get("")
@router.get("/")
def get_bbq_page(request: Request):
    engine, session_id, is_new = get_or_create_bbq(request)
    return render_bbq_state(request, engine, session_id, is_new, "games/bbq.html")


@router.post("/place/{slot_idx}/{food_id}")
def place_food(slot_idx: int, food_id: str, request: Request):
    engine, session_id, is_new = get_or_create_bbq(request)
    engine.place_food(slot_idx, food_id)
    return render_bbq_state(request, engine, session_id, is_new)


@router.post("/flip/{slot_idx}")
def flip_skewer(slot_idx: int, request: Request):
    engine, session_id, is_new = get_or_create_bbq(request)
    engine.flip(slot_idx)
    return render_bbq_state(request, engine, session_id, is_new)


@router.post("/sauce/{slot_idx}")
def brush_sauce(slot_idx: int, request: Request):
    engine, session_id, is_new = get_or_create_bbq(request)
    engine.brush_sauce(slot_idx)
    return render_bbq_state(request, engine, session_id, is_new)


@router.post("/serve/{slot_idx}")
def serve_skewer(slot_idx: int, request: Request):
    engine, session_id, is_new = get_or_create_bbq(request)
    engine.serve(slot_idx)
    return render_bbq_state(request, engine, session_id, is_new)


@router.post("/tick")
def tick_grill(request: Request):
    engine, session_id, is_new = get_or_create_bbq(request)
    engine.tick(1.0)
    return render_bbq_state(request, engine, session_id, is_new)


@router.post("/reset")
def reset_grill(request: Request):
    engine, session_id, is_new = get_or_create_bbq(request)
    engine.reset()
    return render_bbq_state(request, engine, session_id, is_new)
