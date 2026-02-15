---
name: PHP
slug: php
version: 1.0.1
description: 编写高质量的 PHP 代码时，应避免类型转换带来的问题、数组使用上的陷阱以及常见的安全漏洞。
metadata: {"clawdbot":{"emoji":"🐘","requires":{"bins":["php"]},"os":["linux","darwin","win32"]}}
---

## 快速参考

| 主题 | 文件 |
|-------|------|
| 松散类型、`==`、`===`、类型转换、严格类型检查 | `types.md` |
| 关联数组、迭代、数组函数 | `arrays.md` |
| 特性（traits）、接口（interfaces）、可见性（visibility）、延迟静态绑定（late static binding） | `oop.md` |
| 编码（encoding）、字符串插值（string interpolation）、heredoc、正则表达式（regex） | `strings.md` |
| 异常（exceptions）、错误处理（error handling）、`@`操作符 | `errors.md` |
| SQL注入（SQL injection）、XSS攻击（XSS attacks）、CSRF攻击（CSRF attacks）、输入验证（input validation） | `security.md` |
| PHP 8+的新特性、属性（attributes）、命名参数（named arguments）、匹配操作（match operations） | `modern.md` |

## 重要规则

- `==`操作符会强制类型转换：`"0" == false` 的结果是`true`——进行严格比较时请始终使用`===`。
- `in_array($val, $arr)`使用的是宽松类型的比较方式——进行严格比较时请将`true`作为第三个参数传递。
- `strpos()`在字符串开头找到匹配项时会返回0——应使用`=== false`而不是`!strpos()`。
- 绝不要直接拼接SQL语句——请使用PDO的预编译语句（prepared statements）。
- 对所有输出内容使用`htmlspecialchars($s, ENT_QUOTES)`进行转义——以防止XSS攻击。
- `isset()`在变量为`null`时会返回`false`——请使用`array_key_exists()`来检查键是否存在。
- 在`foreach`循环中，使用`&$val`来引用数组元素——循环结束后`$val`会被解引用；如果需要保留引用，请使用`$val = &$val`。
- `static::`表示延迟静态绑定，`self::`表示早期静态绑定——`static`会覆盖父类的方法。
- 使用`@`操作符会抑制错误信息——这会使得调试变得困难，请避免使用。
- 在PHP 7及以上版本中，应该使用`catch (`Throwable`)来捕获`Error`和`Exception`异常。
- 可以在每个文件中通过`declare(strict_types=1)`来启用严格类型检查。
- `strlen()`函数计算的是字符的字节数——对于UTF-8编码的字符串，请使用`mb_strlen()`来获取正确的字符数。
- PHP对象在传递时默认是通过引用传递的——如果需要复制对象，请使用`clone $obj`。
- `array_merge()`在合并数组时会重新生成数字键的索引——如果需要保留原始键，请使用`+`运算符。