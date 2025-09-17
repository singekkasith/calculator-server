from fastapi import APIRouter, Depends
from app.dependancy import get_history, history
from app.schema import CalculatorLog

router = APIRouter(
    prefix="/history",
    tags=["history"],
)

HISTORY_MAX = 1000

# TODO GET /hisory
@router.get("/")
def get_history(limit: int = 50) -> list[CalculatorLog]:
    return list(history)[: max(0, min(limit, HISTORY_MAX))]


@router.delete("/")
def clear_history():
    try:
        history.clear()
        return {"ok": True, "cleared": True} 
    except Exception as e:
        return {"ok": False, "cleared": False, "error":str(e)} 