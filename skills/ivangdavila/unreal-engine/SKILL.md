---
name: Unreal Engine
description: 避免常见的Unreal开发错误——例如垃圾回收（garbage collection）问题、UPROPERTY宏的使用不当、资产复制权限（replication authority）设置错误，以及资产引用（asset reference）相关的陷阱。
metadata: {"clawdbot":{"emoji":"🎯","os":["linux","darwin","win32"]}}
---

## 垃圾回收
- 对于指向`UObject`的原始指针，它们会被垃圾回收机制回收；请使用`UPROPERTY()`来避免这种情况。
- 使用`UPROPERTY()`可以标记变量以便垃圾回收机制进行跟踪；如果不使用该属性，指针可能会变成“悬空”状态（即指向无效的内存）。
- 使用`TWeakObjectPtr`来进行可选的引用；它不能阻止垃圾回收，需要通过`IsValid()`方法来检查引用的对象是否有效。
- 使用`NewObject<T>()`来创建`UObject`；切勿直接使用`new`操作符，因为`new`不会让垃圾回收机制跟踪这些对象。

## UPROPERTY 和 UFUNCTION
- `UPROPERTY()`是蓝图访问和垃圾回收跟踪所必需的。
- `UFUNCTION()`用于蓝图中的可调用函数或事件；同时，它也是数据复制所必需的。
- `EditAnywhere`和`VisibleAnywhere`的区别在于：`EditAnywhere`允许修改对象，而`VisibleAnywhere`仅允许读取对象。
- `BlueprintReadWrite`和`BlueprintReadOnly`用于控制蓝图中的访问权限。

## 演员（Actor）生命周期
- `BeginPlay`在所有组件初始化之后调用；此时可以安全地访问组件。
- 构造函数在类默认对象（CDO，Class Default Object）上执行；此时不要创建演员或访问游戏世界。
- `PostInitializeComponents`在`BeginPlay`之前调用，用于组件的初始化设置。
- `EndPlay`在销毁演员或场景切换时调用，用于资源清理。

## 刷新（Tick）性能优化
- 当不需要时，可以禁用刷新：`PrimaryActorTick.bCanEverTick = false`。
- 使用定时器代替循环刷新：`GetWorldTimerManager().SetTimer()`。
- 使用不同的刷新组来组织代码的执行顺序：`PrePhysics`、`DuringPhysics`、`PostPhysics`。
- 如果蓝图中的刷新逻辑计算复杂，建议将其移至C++代码中执行。

## 数据复制（Replication）
- 服务器拥有数据的所有权；客户端发送请求，服务器验证并复制数据。
- 使用`UPROPERTY(Replicated)`来标记需要同步的变量；需要实现`GetLifetimeReplicatedProps`方法。
- `UFUNCTION(Server)`用于客户端到服务器的远程过程调用（RPC）；这些函数必须是`Reliable`或`Unreliable`类型的。
- 使用`HasAuthority()`方法来检查当前是否在服务器端；在执行服务器端逻辑之前需要先确认这一点。
- `Role`和`RemoteRole`用于判断当前是否在服务器端；`ROLE_Authority`表示当前处于服务器端角色。

## 资产引用
- **硬引用**会加载资产及其父对象，这会导致内存占用增加；仅适用于始终需要使用的资产。
- **软引用`（TSoftObjectPtr`）**按需加载资产；适用于可选或较大的资产。
- 对于软引用，使用`LoadSynchronous()`或`AsyncLoad`方法；确保资产加载完成后再进行访问。
- 在蓝图中引用资产时，可以使用`TSubclassOf<T>`来进行类型安全的对象选择。

## 内存和指针
- `TSharedPtr`用于非`UObject`类型的对象；它会自动管理引用计数并实现自动删除。
- `TUniquePtr`用于确保对象的唯一所有权；不能复制对象，只能移动对象。
- 使用`MakeShared<T>()`来创建对象，并同时管理对象的引用和内存分配。
- 绝不要将原始的`new`和`delete`操作与智能指针混合使用；请选择其中一种模式。

## 常见错误
- 在蓝图中访问`null`演员对象时，请使用`IsValid()`方法进行判断。
- 在编辑器中运行（PIE）和打包后的构建版本可能存在差异；请测试最终发布的构建版本。
- 重新加载蓝图可能会导致蓝图损坏；请关闭编辑器，重新构建后再打开。
- 在构造函数中调用`GetWorld()`时可能返回`null`；此时游戏世界尚未加载，应使用`BeginPlay`方法。
- 在构造函数中创建演员对象可能会导致程序崩溃；请将相关操作推迟到`BeginPlay`之后执行。
- 使用`FString`进行显示文本，使用`FName`作为标识符；`FName`经过哈希处理，比较速度更快。