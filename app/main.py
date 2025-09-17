from collections import deque
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import calculator, history

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calculator.router)
app.include_router(history.router)


'''
# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@app.post("/calculate")
def calculate(expr: Expression):
    try:
        code = expr.expand_percent()
        code = code.replace('÷','/').replace('x','*') 
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr.expr, "result": "", "error": msg}
        # TODO: Add history
        calculator_log = CalculatorLog(
            timestamp= datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            expr= expr.expr,
            result= result)
        history.appendleft(calculator_log)

        return {"ok": True, "expr": expr.expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr.expr, "error": str(e)}

# TODO GET /hisory
@app.get("/history")
def get_history(limit: int = 50) -> list[CalculatorLog]:
    return list(history)[: max(0, min(limit, HISTORY_MAX))]


# TODO DELETE /history
@app.delete("/history")
def clear_history():
    try:
        history.clear()
        return {"ok": True, "cleared": True} 
    except Exception as e:
        return {"ok": False, "cleared": False, "error":str(e)} 

'''