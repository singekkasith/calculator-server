import math
from collections import deque
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter

from calculator import expand_percent
from models import Expression, CalculatorLog

HISTORY_MAX = 1000
history = deque(maxlen=HISTORY_MAX)

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@app.post("/calculate")
def calculate(expr: Expression):
    try:
        code = expr.expand_percent() 
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr.expr, "result": "", "error": msg}
        
        # TODO: Add history
        calculator_log = CalculatorLog(timestamp= datetime.now().strftime("%Y-%m-%d %H:%M:%S"), expr= expr.expr, result= result)
        history.appendleft(calculator_log)

        return {"ok": True, "expr": expr.expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr.expr, "error": str(e)}

# TODO GET /hisory
@app.get("/history")
def get_history(limit: int):
    try:
        if limit < 0:
            limit = 0
        calculator_log = list(history)[:limit]
        return calculator_log;
    except Exception as e:
        return {"error": str(e)}

# TODO DELETE /history
@app.delete("/history")
def clear_history():
    try:
        history.clear()
        return {"ok": True, "cleared": True} 
    except Exception as e:
        return {"ok": False, "cleared": False, "error":str(e)} 

