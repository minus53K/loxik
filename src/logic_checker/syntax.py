# -*- coding: utf-8 -*-
"""
语法模块：基于假言推理（MP）验证证明序列的合法性。
"""

from typing import Tuple
from .parser import stripWhitespace, parseFormula, ParseError


def encodeImplication(A: str, B: str) -> str:
    """
    将蕴含 A -> B 编码为只含 ~ 和 & 的公式：
        (~(A & (~B)))
    输入字符串会被去除空白。
    """
    A_clean = stripWhitespace(A)
    B_clean = stripWhitespace(B)
    return "(~(" + A_clean + "&(~" + B_clean + ")))"


def syntacticProofCheck(theorems: Tuple[str, ...],
                        proof: Tuple[str, ...],
                        axioms: Tuple[str, ...] = ()) -> bool:
    """
    检查 proof 是否是从 theorems 和 axioms 通过假言推理（MP）得到的有效证明。
    每一行必须满足：
        (a) 属于 theorems（精确字符串相等）
        (b) 属于 axioms（精确字符串相等）
        (c) 存在前面的行 i, j 使得 第j行 是 (第i行 -> 当前行) 的编码形式。
    所有公式在比较前会去除空白。
    """
    cleaned_theorems = tuple(stripWhitespace(f) for f in theorems)
    cleaned_axioms = tuple(stripWhitespace(f) for f in axioms)
    cleaned_proof = [stripWhitespace(f) for f in proof]

    # 预先解析所有证明行，若语法错误直接返回 False
    parsed_proof = []
    for f in cleaned_proof:
        try:
            tree = parseFormula(f)
        except ParseError:
            return False
        parsed_proof.append(tree)

    for i, formula_str in enumerate(cleaned_proof):
        valid = False
        # (a) 前提
        if formula_str in cleaned_theorems:
            valid = True
        # (b) 公理
        if not valid and formula_str in cleaned_axioms:
            valid = True
        # (c) MP
        if not valid:
            for j1 in range(i):
                for j2 in range(i):
                    encoded = encodeImplication(cleaned_proof[j1], formula_str)
                    if cleaned_proof[j2] == encoded:
                        valid = True
                        break
                if valid:
                    break
        if not valid:
            return False
    return True