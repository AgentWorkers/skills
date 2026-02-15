---
name: PowerShell
description: 避免常见的 PowerShell 错误：输出行为问题、数组使用错误以及比较运算符的陷阱。
metadata: {"clawdbot":{"emoji":"🔵","requires":{"bins":["pwsh"]},"os":["linux","darwin","win32"]}}
---

## 输出行为
- 所有未捕获的内容都会被输出到控制台——即使没有使用 `return` 或 `Write-Output` 语句。
- `return` 语句不会停止输出；之前的未捕获表达式仍然会被执行并输出。
- `Write-Host` 用于在控制台显示信息，但不用于传递数据。
- 将变量赋值为 `$null` 可以抑制输出：`$null = SomeFunction`。
- 使用 `[void]` 类型转换也可以抑制输出：`[void](SomeFunction)`。

## 数组相关注意事项
- 单个元素的结果是一个标量值，而不是数组：`@(Get-Item .)` 会强制将结果转换为数组。
- 空数组的结果是 `$null`，而不是一个空的数组；请使用 `if ($result)` 来检查结果是否为空。
- 在管道中处理数组时，`@(1,2,3) | ForEach` 会逐个处理数组元素。
- 对数组使用 `+=` 操作会创建一个新的数组；在循环中这样做效率较低，建议使用 `[System.Collections.ArrayList]`。
- `,` 是数组的连接运算符；`,$item` 可以将单个元素包装成数组。

## 比较运算符
- `-eq`、`-ne`、`-gt`、`-lt` 分别表示等于、不等于、大于、小于，而不是 `==`、`!=`、`>`、`<`。
- `-like` 支持通配符，`-match` 支持正则表达式；两者都会返回布尔值。
- `-contains` 用于检查数组中是否包含某个元素：`$arr -contains $item`（注意不是 `$item -in $arr`，尽管 `-in` 也可以使用）。
- 默认情况下比较是不区分大小写的；`-ceq` 和 `-cmatch` 可以进行区分大小写的比较。
- 如果左侧操作数为 `$null`，则使用 `$null -eq $var` 可以避免数组比较时的错误。

## 字符串处理
- 双引号用于字符串插值：`"Hello $name"` 会替换为变量 `$name` 的值。
- 单引号用于表示字面字符串：`'$name'` 会保持原样。
- 对于复杂的字符串表达式，可以使用子表达式：`"Count: $($arr.Count)"` 来获取数组的长度或属性值。
- 多行字符串需要使用 `@" ... "@` 或 `@' ... '@` 的格式。
- 使用反引号来转义特殊字符：``` `n `` 表示换行符，``` `t `` 表示制表符。

## 管道（Pipeline）
- `$_` 或 `$PSItem` 都表示当前处理的对象；`$_` 更常用。
- `ForEach-Object` 用于遍历管道中的对象；`foreach` 语句本身不直接处理管道输入。
- 使用 `-PipelineVariable` 可以保存管道中的中间结果：`Get-Service -PV svc | Where ...`。
- 管道会依次处理每个输入项——除非某个函数支持流式处理。

## 错误处理
- `$ErrorActionPreference` 设置了错误的默认处理方式：`Stop`、`Continue`、`SilentlyContinue`。
- 使用 `-ErrorAction Stop` 可以使非终止性的错误导致脚本终止。
- `try/catch` 仅捕获会导致脚本终止的错误；请先设置 `$ErrorAction Stop`。
- `$?` 表示上一个命令的退出状态；`$LASTEXITCODE` 可用于获取原生命令的退出代码。

## 常见错误
- 在 `if` 语句中，`{` 前面不应有空格：`if($x){` 是正确的写法，而 `if ($x) {` 是错误的写法。
- 在条件语句中，`=` 用于赋值，而比较操作应使用 `-eq`。
- 如果函数返回一个数组，需要使用 `return ,@($arr)` 来保持数组的结构。
- `Get-Content` 返回的是字符串数组；如果需要获取单个字符串，应使用 `-Raw` 选项。
- `Select-Object` 会创建一个新的对象；它返回的是对象的副本，而不是对原始对象的引用。

## 跨平台注意事项
- `pwsh` 是 PowerShell 7 及更高版本的名称；`powershell` 是 Windows PowerShell 5.1 的名称。
- 路径名使用 `/` 或 `\`；`Join-Path` 可以确保路径在所有平台上都能正确解析。
- 环境变量：`$env:VAR` 在所有平台上都有效。
- 不同平台上的 cmdlet 名称可能有所不同；例如 `ls` 和 `cat` 可能在某些平台上不存在，需要使用完整的 cmdlet 名称。