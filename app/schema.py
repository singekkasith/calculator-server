import re
from datetime import datetime
from pydantic import BaseModel
from typing import Any

_percent_pair = re.compile(r"""
    (?P<a>\d+(?:\.\d+)?)
    \s*(?P<op>[+\-*/])\s*
    (?P<b>\d+(?:\.\d+)?)%
""", re.VERBOSE)
_number_percent = re.compile(r"(?P<n>\d+(?:\.\d+)?)%")

class BaseExpression(BaseModel):
    expr: str

class Expression(BaseExpression): #ExpressionIn
    '''expand_percent() method is already in dependency.py'''
    pass

class CalculatorLog(Expression): #ExpressionOut
    result : Any
    timestamp: str = datetime.now().isoformat() + "Z"

