# Loxik —— 一个命题逻辑公式解析器

这是一个测试项目，是我用来熟悉代码写作流程和命题逻辑基础的。

项目的名字源于西班牙语的“逻辑”的逻辑语化读音，'x'读作国际音标中的/x/（汉语拼音中的'h'）

## 功能

- **语义蕴含判定**：输入定理集和结论，自动枚举所有可能的真值赋值，判断是否语义蕴含。
- **语法证明验证**：输入定理集和证明序列，基于 **假言推理规则（Modus Ponens）** 逐行检查证明是否合法（支持公理扩展接口）。

## 语法规则

本项目使用**严格全括号**语法（括号不能省略），解析前会自动忽略所有空白字符：

| 类型 | 格式 | 示例 |
| :--- | :--- | :--- |
| 原子公式 | 单个小写字母 | `a` |
| 否定式 | `(~X)` | `(~a)` 、 `(~(a&b))` |
| 合取式 | `(X&Y)` | `(a&b)` 、 `((~a)&b)` |

## 快速示例

```python
# 引入公理集
theorems = ("a", "(~(a&(~b)))")  # a 和 a->b

# 语义蕴含判定：a, a->b 能否推出 b ?
from logic_checker import isSemanticEntailment
conclusion = "b"
print(isSemanticEntailment(theorems, conclusion))  # 输出: True

# 语法证明验证：检查给定的证明序列是否正确
from logic_checker import isValidProof
proof = ("a", "(~(a&(~b)))", "b")  # 利用 MP 推出 b
print(isValidProof(theorems, proof))  # 输出: True
```

## 许可证
本项目采用 [MIT License](https://license/) 开源协议。