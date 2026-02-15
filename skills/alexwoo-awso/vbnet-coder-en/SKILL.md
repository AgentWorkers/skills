# VB.NET 编码代理技能参考

**目标**：Claude-Code、Codex、AI 编码代理  
**版本**：2026 Modern .NET  
**最大代码行数**：500 行  

---

## 详细参考资料  

有关特定主题的详细模式、示例和最佳实践，请参阅：  

| 主题 | 文件 | 查阅时机 |  
|-------|------|-----------------|  
| 类型系统 | [docs/types-and-declarations.md](docs/types-and-declarations.md) | 变量声明、可空类型、字段声明 |  
| 控制流 | [docs/control-flow.md](docs/control-flow.md) | If/ElseIf、Select Case、循环、Exit/Continue |  
| 异步/等待 | [docs/async-patterns.md](docs/async-patterns.md) | 异步方法结构、ConfigureAwait、取消操作、Task.WhenAll |  
| 错误处理 | [docs/error-handling.md](docs/error-handling.md) | 异常处理、Try/Catch/Finally、IDisposable、Using 语句 |  
| LINQ | [docs/linq-patterns.md](docs/linq-patterns.md) | 查询/方法语法、常见操作、延迟执行 |  
| 字符串与集合 | [docs/strings-and-collections.md](docs/strings-and-collections.md) | 字符串比较与构建、List、Dictionary、HashSet、数组 |  
| 类设计与模式 | [docs/class-design-and-patterns.md](docs/class-design-and-patterns.md) | 属性、构造函数、接口、工厂模式、Repository、空对象模式 |  

---

## 关键的编译器指令  

### 必须在每个文件顶部包含的文件头：  

```vb
Option Explicit On
Option Strict On
Option Infer On
```  

**理由**：  
- `Option Explicit On` 可防止使用未声明的变量（避免拼写错误）；  
- `Option Strict On` 可确保类型安全（防止隐式转换导致的运行时错误）；  
- `Option Infer On` 可在保持类型安全的同时启用局部类型推断。  

**切勿使用**：`Option Explicit Off` 或 `Option Strict Off`——这些设置会导致运行时错误、性能下降以及晚期绑定开销。  

**建议在项目级别设置**：尽可能在 `.vbproj` 文件中设置这些选项，而不是在每个文件中单独设置。  

---

## 命名约定  

### 核心规则  

| 元素 | 命名规则 | 示例 |  
|---------|-----------|---------|  
| **命名空间** | 使用 PascalCase，采用层次结构 | `CompanyName.ProductName.ComponentName` |  
| **类/接口** | 使用 PascalCase，采用名词/名词短语的形式 | `CustomerRepository`、`IPaymentProcessor` |  
| **接口前缀** | 以 `I` 开头 | `IDisposable`、`IEnumerable(Of T)` |  
| **方法** | 使用 PascalCase，采用动词/动词短语的形式 | `CalculateTotal()`、`ProcessPayment()` |  
| **属性** | 使用 PascalCase，采用名词/形容词的形式 | `CustomerName`、`IsActive` |  
| **字段（私有）** | 使用下划线分隔的驼峰式命名法 | `_connectionString`、`_maxRetries` |  
| **字段（公有/共享）** | 使用 PascalCase | `MaxValue`、`DefaultTimeout` |  
| **参数/局部变量** | 使用驼峰式命名法 | `userId`、`itemCount` |  
| **常量** | 使用 PascalCase 或大写蛇形命名法 | `MaxConnections`、`DEFAULT_TIMEOUT` |  
| **枚举类型** | 使用 PascalCase，采用单数形式 | `OrderStatus`、`FileMode` |  
| **枚举成员** | 使用 PascalCase | `OrderStatus.Pending`、`FileMode.Read` |  
| **事件** | 使用 PascalCase，采用动词短语的形式 | `DataReceived`、`ConnectionClosed` |  
| **委托** | 使用 PascalCase，以 `Handler` 或 `Callback` 结尾 | `EventHandler`、`DataReceivedCallback` |  
| **泛型参数** | 使用 `T + PascalCase` 的形式 | `TKey`、`TValue`、`TEntity` |  

### 具体指南  

- **布尔值相关的方法名**：使用 `Is`、`Has`、`Can`、`Should` 等前缀。  
- **集合/数组的命名**：使用复数名词。  
- **异步方法**：方法名后必须加上 `Async` 后缀。  
- **避免使用匈牙利命名法（如 `strName`、`intCount`）以及 `My` 前缀（可能与 VB.NET 的 `My` 命名空间冲突）；除非是广为人知的缩写（例如 `Id`、`Xml`、`Http`），否则应避免使用缩写。  

---

## 代码布局与风格  

### 缩进与间距  
- 每个缩进级别使用 4 个空格（禁止使用制表符）  
- 每行只包含一个语句  
- 方法/属性之间使用空行  
- 在可能的情况下，使用隐式换行（无需使用下划线）  

```vb
' ✓ Implicit line continuation (no underscore needed)
Dim result = customers _
    .Where(Function(c) c.IsActive) _
    .OrderBy(Function(c) c.Name) _
    .ToList()

Dim customer = New Customer With {
    .Name = "John",
    .Email = "john@example.com",
    .IsActive = True
}

' Method parameters
Public Function ProcessOrder(
    orderId As Integer,
    customerId As Integer,
    processDate As Date) As OrderResult
```  

### 注释  
```vb
' Single-line comment for brief explanations

''' <summary>
''' Processes customer orders asynchronously.
''' </summary>
''' <param name="customerId">The unique customer identifier.</param>
''' <param name="cancellationToken">Token to cancel the operation.</param>
''' <returns>A task representing the async operation with the order result.</returns>
''' <exception cref="CustomerNotFoundException">Thrown when customer not found.</exception>
Public Async Function ProcessOrdersAsync(
    customerId As Integer,
    cancellationToken As CancellationToken) As Task(Of OrderResult)

    ' Implementation
End Function
```  

**避免**：对显而易见的代码添加注释、冗余注释，以及被注释掉的代码（这些代码应通过版本控制来管理）。  

---

## 文件组织结构  

**标准文件结构**：  
```vb
Option Explicit On
Option Strict On
Option Infer On

Imports System
Imports System.Collections.Generic
Imports System.Linq
Imports System.Threading.Tasks

Namespace CompanyName.ProjectName.ComponentName

    ''' <summary>
    ''' Brief class description.
    ''' </summary>
    Public Class ClassName
        ' Constants
        Private Const DefaultTimeout As Integer = 30

        ' Shared (static) fields
        Public Shared ReadOnly MaxConnections As Integer = 100

        ' Private fields
        Private _connectionString As String
        Private ReadOnly _logger As ILogger

        ' Constructors
        Public Sub New(logger As ILogger)
            _logger = logger
        End Sub

        ' Properties
        Public Property Name As String

        ' Methods
        Public Function DoSomething() As Integer
            ' Implementation
        End Function

        ' IDisposable implementation if needed
        Public Sub Dispose() Implements IDisposable.Dispose
            ' Cleanup
        End Sub
    End Class
End Namespace
```  

---

## 性能考虑  

- **避免装箱/拆箱操作**：优先使用泛型而非 `Object` 类型的集合。  
- **字符串比较**：当文化环境无关紧要时，使用 `StringComparisonOrdinal` 以提高性能。  
- **LINQ 操作**：仅在需要时才调用 `.ToList()`，并利用延迟执行机制。  
- **异步 I/O**：对于文件、数据库、网络操作，始终使用异步处理。  
- **ConfigureAwait(False)**：在库代码中使用该选项，以避免同步上下文带来的开销。  
- **StringBuilder**：在循环中连接多个字符串时使用 `StringBuilder`。  
- **集合容量**：在已知集合大小的情况下，为 `List(Of T)` 和 `Dictionary(Of K, V)` 设置初始容量。  

```vb
Dim customers As New List(Of Customer)(expectedCount)  ' Avoid reallocations
```  

---

## 应避免的常见不良编码习惯  

❌ **禁用 `Option Strict`**——会导致运行时错误和性能问题。  
❌ **编写 `Async void` 方法**——这些方法无法捕获异常（事件处理程序除外）。  
❌ **编写阻塞式的异步代码**——使用 `.Result` 或 `.Wait()` 可能导致死锁。  
❌ **捕获异常时不进行日志记录**——会导致错误被忽略。  
❌ **不释放 `IDisposable` 对象**——会导致内存或资源泄漏。  
❌ **使用 `==` 进行字符串比较**——这种做法依赖于文化环境，应使用 `.Equals()` 和 `StringComparison`。  
❌ **在循环中进行字符串连接**——会导致 O(n²) 的性能开销。  
❌ **不使用 `Using` 语句**——异常发生时资源可能无法被释放。  
❌ **使用匈牙利命名法**——这种命名方式已经过时，不符合现代编码风格。  
❌ **使用魔法数字**——应使用有意义的常量。  
❌ **代码结构过于复杂（深度嵌套）**——应提取方法或提前返回结果。  

---

## 代理特定的编码指南  

**在生成 VB.NET 代码时，请遵循以下规则：**  
1. **在文件顶部始终添加 `Option Explicit On` 和 `Option Strict On`。  
2. **所有声明都应使用显式类型。**  
3. **优先使用 LINQ 方法语法（便于代理解析）。  
4. **对于 `IDisposable` 对象，务必使用 `Using` 语句。**  
5. **所有 I/O 操作都应使用异步处理。**  
6. **为公共 API 提供 XML 文档。**  
7. **使用有意义的变量名**——优先考虑代码的可读性而非简洁性。  
8. **显式处理异常**——避免使用空catch语句。  
9. **严格遵循命名约定**——公有成员使用 PascalCase，私有成员使用驼峰式命名法。  
10. **每个方法只负责一个功能**——当逻辑变得复杂时，应将其拆分为多个方法。  
11. **优先使用组合而非继承**——尽量使用接口。  
12. **尽可能保持数据不可变**——使用只读字段和只读属性。  
13. **在方法入口处验证参数。**  
14. **对于耗时的异步操作，使用 `CancellationToken`。**  
15. **记录异常时附带相关上下文信息**——在日志中包含关键数据。  

---

**技能参考结束**  

*本文档专为 AI 编码代理设计，旨在生成符合 .NET Framework 4.8+ 及 .NET 6/7/8+ 标准的现代、可维护的 VB.NET 代码。*