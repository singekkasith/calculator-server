
from pydantic import BaseModel
from calculator import expand_percent
from typing import Optional

class Expression(BaseModel):
    expr: Optional[str] = None  

    def expand_percent(self) -> str:
        if not self.expr:
            return ""
        return expand_percent(self.expr)

class CalculatorLog(BaseModel):
    timestamp: str
    expr : str
    result : float

