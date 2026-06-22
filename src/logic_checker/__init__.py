# -*- coding: utf-8 -*-
"""
命题逻辑解析器 - 顶层接口。
"""

from .semantics import semanticEntailment
from .proof_checker import syntacticProofCheck
from .parser import ParseError


__all__ = [
    "semanticEntailment",
    "syntacticProofCheck",
    "ParseError",
]