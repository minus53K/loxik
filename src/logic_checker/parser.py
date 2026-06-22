# -*- coding: utf-8 -*-
"""
解析模块：提供公式处理（删除空白字符和检查公式是否合法）和解析（构建语法树）功能。
"""

class ParseError(Exception):
    pass


def stripWhitespace(s: str) -> str:
    """删除字符串中的所有空白字符（空格、制表符、换行等）"""
    return ''.join(s.split())


def isLowercaseLetter(c: str) -> bool:
    """判断字符是否为小写字母"""
    return 'a' <= c <= 'z'


def parseFormula(s: str) -> tuple:
    """
    删去字符串中的空白字符，并判断是否为合法公式，如果是则返回语法树。
    语法：
        formula := atom | '(' '~' formula ')' | '(' formula '&' formula ')'
        atom    := 小写字母（a-z）
    """
    s = stripWhitespace(s)
    if not s:
        raise ParseError("输入的公式为空")
    tree, remaining = parseExpression(s)
    if remaining:
        raise ParseError(f"公式后有多余字符: {remaining}")
    return tree


def parseExpression(s: str) -> tuple:
    """
    用递归下降法解析一个公式，返回语法树和剩余字符串

    示例：假设传入字符串'(a&(~b))'，那么：
    1. 识别最外层括号，得到inner为'a&(~b))'
    2. inner[0]为'a'，判断为合取情形，再次调用函数，现在要解析'a&(~b))'
    3. 解析在'a'终止，返回'a'和'&(~b))'，再次调用函数，现在要解析'(~b))'
    4. 识别最外层括号，得到inner为'~b))'
    5. inner[0]为'~'，判断为否定情形，再次调用函数，现在要解析'b))'
    6. 解析在'b'终止，返回'b'和'))'，回到否定情形，检查剩余字符串')'，正确，返回('~', 'b')和')'
    7. 回到合取情形，检查剩余字符串')'，正确，返回('&', 'a', ('~', 'b'))和空字符串

    由于每次递归调用都会消耗至少一个字符，可以在有限步内得到解析结果
    """
    if not s:
        raise ParseError("意外的公式结束")

    # 情况1: 原子（小写字母）
    if isLowercaseLetter(s[0]):
        return s[0], s[1:]

    # 情况2: 复合公式，必须以 '(' 开头
    if s[0] != '(':
        raise ParseError(f"公式开头期望 '(' 或原子（小写字母），但得到 '{s[0]}'")

    inner = s[1:]
    if not inner:
        raise ParseError("括号内为空")

    if inner[0] == '~':
        # 否定情形: (~X)
        sub, rest0 = parseExpression(inner[1:])
        if not rest0:
            raise ParseError("否定式缺少右括号")
        if rest0[0] != ')':
            raise ParseError(f"否定式期望 ')'，但得到 '{rest0[0]}'")
        return ('~', sub), rest0[1:]
    else:
        # 合取情形: (X&Y)
        left, rest0 = parseExpression(inner)
        if not rest0:
            raise ParseError("合取式缺少运算符")
        if rest0[0] != '&':
            raise ParseError(f"合取式期望 '&'，但得到 '{rest0[0]}'")
        right, rest1 = parseExpression(rest0[1:])
        if not rest1:
            raise ParseError("合取式缺少右括号")
        if rest1[0] != ')':
            raise ParseError(f"合取式期望 ')'，但得到 '{rest1[0]}'")
        return ('&', left, right), rest1[1:]