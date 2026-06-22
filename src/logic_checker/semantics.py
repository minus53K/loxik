# -*- coding: utf-8 -*-
"""
语义模块：提供对语法树的真值表枚举和语义蕴含判定功能。
"""

import itertools
from typing import Tuple, Dict, Set
from .parser import parseFormula, ParseError


def collectVariables(tree) -> Set[str]:
    """
    递归收集语法树中的所有变量名
    语法树是波兰表达式的形式，可以方便地进行遍历和分析
    """
    if isinstance(tree, str):
        return {tree}
    elif isinstance(tree, tuple):
        op = tree[0]
        if op == '~':
            return collectVariables(tree[1])
        elif op == '&':
            return collectVariables(tree[1]) | collectVariables(tree[2])
        else:
            raise ValueError(f"未知节点类型: {op}")
    else:
        raise TypeError(f"无效树节点: {tree}")


def evaluate(tree, assignment: Dict[str, bool]) -> bool:
    """
    在给定赋值下计算公式的真值
    赋值是一个字典，映射变量名到布尔值
    最终得到的是整个表达式在特定赋值下的真值
    """
    if isinstance(tree, str):
        return assignment[tree]
    elif isinstance(tree, tuple):
        op = tree[0]
        if op == '~':
            return not evaluate(tree[1], assignment)
        elif op == '&':
            return evaluate(tree[1], assignment) and evaluate(tree[2], assignment)
        else:
            raise ValueError(f"未知运算符: {op}")
    else:
        raise TypeError(f"无效树节点: {tree}")


def semanticEntailment(theorems: Tuple[str, ...], conclusion: str) -> bool:
    """
    判断 theorem 元组是否语义蕴含 conclusion。
    真值表穷举所有出现在 theorems 和 conclusion 中的变量。
    若输入公式语法错误，返回 False（不蕴含）。
    """
    try:
        parsed_theorems = [parseFormula(f) for f in theorems]
        parsed_concl = parseFormula(conclusion)
    except ParseError:
        return False

    vars_set: Set[str] = set()
    for t in parsed_theorems:
        vars_set |= collectVariables(t)
    vars_set |= collectVariables(parsed_concl)
    variables = sorted(vars_set)

    for values in itertools.product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        if all(evaluate(t, assignment) for t in parsed_theorems):
            if not evaluate(parsed_concl, assignment):
                return False
    return True