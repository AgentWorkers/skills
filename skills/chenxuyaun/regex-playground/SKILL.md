---
name: regex-playground
description: 学习、测试和调试正则表达式，支持实时匹配功能，并提供详细解释及常见使用模式。非常适合正在学习正则表达式或需要调试复杂正则表达式的开发者。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": [] },
        "install": [],
      },
  }
---
# 正则表达式练习场

这是一个用于交互式学习与测试正则表达式的工具。

## 使用方法

```
regex "pattern" "test string"
```

## 主要功能

- 🎯 实时匹配功能：可以实时查看正则表达式的匹配结果。
- 📖 通俗易懂的解释：为每个正则表达式提供详细的中文说明。
- 🔍 匹配组提取：帮助用户了解匹配过程中的各个组（groups）。
- 📋 常见模式库：收录了常用的正则表达式模式。
- 🧪 测试用例生成器：能够自动生成针对不同类型的输入数据的测试用例。

## 示例

```
Input: regex "(\w+)@(\w+)\.(\w+)" "test@example.com"

Output:
✓ Match: test@example.com
Group 1: test
Group 2: example  
Group 3: com

Explanation:
- (\w+) - capture word characters (test)
- @ - literal @
- (\w+) - capture word characters (example)
- \. - literal dot
- (\w+) - capture word characters (com)
```

## 常见正则表达式模式

| 模式            | 含义                                      | 示例                                      |
|-----------------|-----------------------------------------|-----------------------------------------|
| `\d+`            | 一个或多个数字                              | 123                                      |
| `\w+`            | 一个或多个字母或数字                              | hello_123                                   |
| `[a-z]`            | 一个或多个小写字母                              | a, b, c                                   |
| `^start`          | 以 “start” 开头                              | start...                                |
| `end$`          | 以 “end” 结尾                              | ...end                                   |
| `a|b`            | “a” 或 “b”                                  | a 或 b                                   |
| `a*`            | 零个或多个 “a”                                | '', a, aaa                                   |
| `a+`            | 一个或多个 “a”                                | a, aaa                                   |

## 命令

- `regex explain <pattern>`          | 用通俗易懂的语言解释指定的正则表达式模式。          |
- `regex test <pattern> <string>`       | 使用指定的正则表达式测试输入字符串。          |
- `regex library`         | 显示所有可用的正则表达式模式。                |
- `regex generate <type>`         | 生成针对特定类型的输入数据（如电子邮件、网址、电话号码等）的测试用例。 |

## 使用场景

- 在代码中调试正则表达式问题。
- 通过观察匹配结果来学习正则表达式的使用方法。
- 验证输入数据是否符合预定的模式。
- 从字符串中提取所需的信息。