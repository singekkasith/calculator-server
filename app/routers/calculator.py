import math
from datetime import datetime
from typing import Callable, List
from asteval import Interpreter

from fastapi import APIRouter, Depends

from app.dependancy import expand_percent, get_history, history
from app.schema import CalculatorLog, Expression

router = APIRouter(
    prefix="/calculate",
    tags=["calculate"],
)

# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})

@router.post("/")
def calculate(expr: Expression, expand_func: Callable[[str],str] = Depends(lambda: expand_percent)):
    try:
        code = expand_percent(expr.expr)
        code = code.replace('÷','/').replace('x','*') 
        result = aeval(code)

        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr.expr, "result": "", "error": msg}
        
        # TODO: Add history
        calculator_log = CalculatorLog(
            timestamp= datetime.now().isoformat() + "Z",
            expr= expr.expr,
            result= result)
        history.appendleft(calculator_log)

        return {"ok": True, "expr": expr.expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr.expr, "error": str(e)}