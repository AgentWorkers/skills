---
name: Roblox
description: 避免常见的 Roblox 开发错误：服务器/客户端安全问题、DataStore 使用中的陷阱、内存泄漏以及数据复制相关的常见问题。
metadata: {"clawdbot":{"emoji":"🎲","os":["linux","darwin","win32"]}}
---

## 服务器与客户端  
- `ServerScriptService` 中的服务器脚本：切勿信任客户端发送的数据。  
- `StarterPlayerScripts` 或 `StarterGui` 中的本地脚本：仅适用于客户端。  
- 对于“发送数据后无需响应”的场景，使用 `RemoteEvent`；如果服务器需要返回数据，则使用 `RemoteFunction`。  
- **务必在服务器端进行所有数据验证**——客户端可以发送任何内容，攻击者可能会利用这些漏洞。  

## 安全性  
- **切勿信任客户端输入**——所有数据都应在服务器端进行验证。  
- **服务器端应进行合理性检查**：玩家是否有权限访问该数据？数据是否在合理范围内？  
- `FilteringEnabled` 始终处于开启状态，但这并不能保护 `RemoteEvents` 的安全性；请在服务器端检查权限。  

## 数据存储  
- `:GetAsync()` 和 `:SetAsync()` 可能会失败；应使用 `pcall` 包装这些方法，并设置重试机制（例如采用退避策略）。  
- 请求速率限制：每分钟最多 60 + `numPlayers × 10` 次请求；尽可能批量处理写入操作。  
- 使用 `:UpdateAsync()` 进行读-修改-写操作，以防止竞态条件。  
- 实施会话锁定机制，避免玩家重新连接时数据丢失；使用 `:UpdateAsync()` 并进行相应的检查。  
- 使用 Studio API 进行测试：设置 → 安全 → API 服务。  

## 内存泄漏  
- 确保连接在操作完成后被正确断开（使用 `:Disconnect()`）。  
- 当对象被删除时，应调用 `:Destroy()` 方法，将对象的 `Parent` 属性设置为 `nil` 并断开相关事件连接。  
- 如果玩家离开游戏但没有进行清理操作，应通过 `Players.PlayerRemoving` 事件进行清理。  
- 对于包含引用的数据结构，应移除不再需要的引用（将引用设置为 `nil`）。  

## 角色处理  
- 在 `PlayerAdded` 事件触发时，角色可能尚未创建；请使用 `player.CharacterAdded:Wait()` 或相关事件进行等待。  
- 角色重生时，应重新连接并触发 `CharacterAdded` 事件。  
- 当角色死亡时，会触发 `Humanoid.Died` 事件，以便执行死亡处理逻辑。  
- 可以使用 `LoadCharacter()` 强制角色重生，但通常建议让角色自然重生。  

## 数据复制  
- `ServerStorage` 仅存在于服务器端，客户端无法访问。  
- `ReplicatedStorage` 可被服务器和客户端同时访问，用于共享模块和资源。  
- `ReplicatedFirst` 机制确保客户端首先加载相关数据（例如加载界面时）。  
- 工作区数据会复制到客户端，但服务器拥有最终数据控制权。  

## 服务模式  
- 使用 `game:GetService("ServiceName")` 来获取服务；避免直接通过索引访问，否则可能在不同环境下导致错误。  
- 使用缓存机制来存储服务引用（例如：`local Players = game:GetService("Players")`）。  
- 常用服务包括 `Players`、`ReplicatedStorage`、`ServerStorage`、`RunService` 和 `DataStoreService`。  

## `RunService` 的工作流程  
- `Heartbeat` 事件在物理计算之后执行，包含大部分游戏逻辑。  
- `RenderStepped` 事件仅在客户端触发，用于更新渲染相关内容（如摄像机位置、视觉效果等）。  
- `Stepped` 事件在物理计算之前执行，用于处理游戏对象的移动等操作。  
- 避免在每一帧都进行复杂的计算，可将计算任务分散到多个帧中执行。  

## 常见错误  
- `wait()` 方法已被弃用，建议使用 `task.wait()` 来实现可靠的延迟控制。  
- `spawn()` 方法已被弃用，建议使用 `taskspawn()` 或 `task.defer()` 来延迟任务执行。  
- 模块之间的依赖关系会导致数据缓存问题；确保依赖关系中的数据是共享的。  
- `:Clone()` 方法不会自动触发相关事件；如有需要，请手动触发这些事件。  
- 即使对象的 `CanCollide` 属性设置为 `false`，碰撞检测事件（如 `Touched`）仍会触发；建议使用 `CanTouch` 方法进行判断。