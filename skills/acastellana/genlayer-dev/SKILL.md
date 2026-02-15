---
name: genlayer-dev-claw-skill
version: 1.0.0
description: **构建 GenLayer 智能合约**  
这些 Python 智能合约支持与大型语言模型（LLM）的交互以及网络访问功能。内容包括合约的编写与部署方法、SDK 参考文档、命令行工具（CLI）的使用说明、相关原理以及数据存储类型。  

**可使用的命令/工具：**  
- `write_intelligent_contract`：用于编写智能合约  
- `genlayer_contract`：生成 GenLayer 合约  
- `genvm`  
- `gl.Contract`  
- `deploy_genlayer`：部署 GenLayer 合约  
- `genlayerCLI`：GenLayer 的命令行工具  
- `genlayerSDK`：GenLayer 的 SDK  
- `DynArray`  
- `TreeMap`  
- `gl.nondet`  
- `gl.eq_principle`  
- `prompt_comparative`  
- `strict_eq`  
- `genlayer_deploy`  
- `genlayer_up`  

**说明：**  
若需详细了解 GenLayer 的概念，建议使用 `genlayer-claw-skill` 进行查阅。
---

# GenLayer 智能合约

GenLayer 支持 **智能合约**——这些基于 Python 的智能合约能够调用大型语言模型（LLMs），获取网络数据，并在保持区块链共识的同时处理非确定性操作。

## 快速入门

### 最小化合约示例
```python
# v0.1.0
# { "Depends": "py-genlayer:latest" }
from genlayer import *

class MyContract(gl.Contract):
    value: str
    
    def __init__(self, initial: str):
        self.value = initial
    
    @gl.public.view
    def get_value(self) -> str:
        return self.value
    
    @gl.public.write
    def set_value(self, new_value: str) -> None:
        self.value = new_value
```

### 与大型语言模型交互的合约
```python
# v0.1.0
# { "Depends": "py-genlayer:latest" }
from genlayer import *
import json

class AIContract(gl.Contract):
    result: str
    
    def __init__(self):
        self.result = ""
    
    @gl.public.write
    def analyze(self, text: str) -> None:
        prompt = f"Analyze this text and respond with JSON: {text}"
        
        def get_analysis():
            return gl.nondet.exec_prompt(prompt)
        
        # All validators must get the same result
        self.result = gl.eq_principle.strict_eq(get_analysis)
    
    @gl.public.view
    def get_result(self) -> str:
        return self.result
```

### 具有网络访问功能的合约
```python
# v0.1.0
# { "Depends": "py-genlayer:latest" }
from genlayer import *

class WebContract(gl.Contract):
    content: str
    
    def __init__(self):
        self.content = ""
    
    @gl.public.write
    def fetch(self, url: str) -> None:
        url_copy = url  # Capture for closure
        
        def get_page():
            return gl.nondet.web.render(url_copy, mode="text")
        
        self.content = gl.eq_principle.strict_eq(get_page)
    
    @gl.public.view
    def get_content(self) -> str:
        return self.content
```

## 核心概念

### 合约结构
1. **版本头部**: `# v0.1.0`（必需）
2. **依赖项**: `# { "Depends": "py-genlayer:latest" }`
3. **导入**: `from genlayer import *`
4. **类**: 继承自 `gl.Contract`（每个文件中只能有一个此类）
5. **状态**: 类级别的类型化属性
6. **构造函数**: `__init__`（非公共方法）
7. **方法**: 使用 `@gl.public.view` 或 `@gl.public.write` 装饰器进行修饰

### 方法装饰器
| 装饰器 | 用途 | 是否可以修改状态 |
|-----------|---------|------------------|
| `@gl.public.view` | 仅用于读取操作 | 不可以 |
| `@gl.public.write` | 可以修改状态 | 可以 |
| `@gl.public.write.payable` | 可以接收输入并修改状态 | 可以 |

### 存储类型
将标准 Python 类型替换为 GenVM 兼容的存储类型：

| Python 类型 | GenVM 类型 | 用途 |
|-------------|------------|-------|
| `int` | `u32`, `u64`, `u256`, `i32`, `i64` 等 | 带大小的整数 |
| `int`（无限制） | `bigint` | 避免使用，因为精度可能不准确 |
| `list[T]` | `DynArray[T]` | 动态数组 |
| `dict[K,V]` | `TreeMap[K,V]` | 有序映射 |
| `str` | `str` | 字符串（保持不变） |
| `bool` | `bool` | 布尔值（保持不变） |

**⚠️ 不支持使用 `int` 类型！** 请始终使用带大小的整数类型。

### 地址类型
```python
# Creating addresses
addr = Address("0x03FB09251eC05ee9Ca36c98644070B89111D4b3F")

# Get sender
sender = gl.message.sender_address

# Conversions
hex_str = addr.as_hex      # "0x03FB..."
bytes_val = addr.as_bytes  # bytes
```

### 自定义数据类型
```python
from dataclasses import dataclass

@allow_storage
@dataclass
class UserData:
    name: str
    balance: u256
    active: bool

class MyContract(gl.Contract):
    users: TreeMap[Address, UserData]
```

## 非确定性操作

### 问题
大型语言模型和网络请求在不同验证节点上可能会产生不同的结果。GenLayer 通过 **等价性原则** 来解决这个问题。

### 等价性原则

#### 1. **严格相等 (`strict_eq`)**
所有验证节点必须产生 **完全相同** 的结果。
```python
def get_data():
    return gl.nondet.web.render(url, mode="text")

result = gl.eq_principle.strict_eq(get_data)
```

适用于：事实性数据、布尔值结果、精确匹配的情况。

#### 2. **提示比较 (`prompt_comparative)`
大型语言模型会根据特定标准将领导节点的结果与其他验证节点的结果进行比较。
```python
def get_analysis():
    return gl.nondet.exec_prompt(prompt)

result = gl.eq_principle.prompt_comparative(
    get_analysis,
    "The sentiment classification must match"
)
```

适用于：需要语义等价性的大型语言模型任务。

#### 3. **提示非比较 (`prompt_non_comparative)`
验证节点只需验证领导节点的结果是否符合标准，无需重新执行操作。
```python
result = gl.eq_principle.prompt_non_comparative(
    lambda: input_data,  # What to process
    task="Summarize the key points",
    criteria="Summary must be under 100 words and factually accurate"
)
```

适用于：计算成本较高的操作或主观性较强的任务。

#### 4. 自定义领导节点/验证节点模式
```python
result = gl.vm.run_nondet(
    leader=lambda: expensive_computation(),
    validator=lambda leader_result: verify(leader_result)
)
```

### 非确定性函数

| 函数 | 用途 |
|----------|---------|
| `gl.nondet.exec.prompt(prompt)` | 执行大型语言模型的提示 |
| `gl.nondet.web.render(url, mode)` | 获取网页内容（`mode="text"` 或 `"html"`）

**⚠️ 规则：**
- 必须在等价性原则相关的函数内部调用这些函数。
- 不能直接访问存储数据。
- 需要先使用 `gl.storage.copy_to_memory()` 将存储数据复制到内存中。

## 合约交互

### 调用其他合约
```python
# Dynamic typing
other = gl.get_contract_at(Address("0x..."))
result = other.view().some_method()

# Static typing (better IDE support)
@gl.contract_interface
class TokenInterface:
    class View:
        def balance_of(self, owner: Address) -> u256: ...
    class Write:
        def transfer(self, to: Address, amount: u256) -> bool: ...

token = TokenInterface(Address("0x..."))
balance = token.view().balance_of(my_address)
```

### 发送消息（异步调用）
```python
other = gl.get_contract_at(addr)
other.emit(on='accepted').update_status("active")
other.emit(on='finalized').confirm_transaction()
```

### 部署合约
```python
child_addr = gl.deploy_contract(code=contract_code, salt=u256(1))
```

### 与以太坊虚拟机（EVM）的互操作性
```python
@gl.evm.contract_interface
class ERC20:
    class View:
        def balance_of(self, owner: Address) -> u256: ...
    class Write:
        def transfer(self, to: Address, amount: u256) -> bool: ...

token = ERC20(evm_address)
balance = token.view().balance_of(addr)
token.emit().transfer(recipient, u256(100))  # Messages only on finality
```

## 命令行接口（CLI）命令

### 设置
```bash
npm install -g genlayer
genlayer init      # Download components
genlayer up        # Start local network
```

### 合约部署
```bash
# Direct deploy
genlayer deploy --contract my_contract.py

# With constructor args
genlayer deploy --contract my_contract.py --args "Hello" 42

# To testnet
genlayer network set testnet-asimov
genlayer deploy --contract my_contract.py
```

### 合约交互
```bash
# Read (view methods)
genlayer call --address 0x... --function get_value

# Write
genlayer write --address 0x... --function set_value --args "new_value"

# Get schema
genlayer schema --address 0x...

# Check transaction
genlayer receipt --tx-hash 0x...
```

### 网络连接
```bash
genlayer network                    # Show current
genlayer network list               # Available networks
genlayer network set localnet       # Local dev
genlayer network set studionet      # Hosted dev
genlayer network set testnet-asimov # Testnet
```

## 最佳实践

### 提示设计
```python
prompt = f"""
Analyze this text and classify the sentiment.

Text: {text}

Respond using ONLY this JSON format:
{{"sentiment": "positive" | "negative" | "neutral", "confidence": float}}

Output ONLY valid JSON, no other text.
"""
```

### 安全性：提示注入
- **限制输入**：减少用户可控文本在提示中的使用量。
- **限制输出**：明确指定输出格式。
- **验证**：检查解析后的结果是否符合预期格式。
- **简化逻辑**：清晰的合约流程可以降低攻击风险。

### 错误处理
```python
from genlayer import UserError

@gl.public.write
def safe_operation(self, value: int) -> None:
    if value <= 0:
        raise UserError("Value must be positive")
    # ... proceed
```

### 内存管理
```python
# Copy storage to memory for non-det blocks
data_copy = gl.storage.copy_to_memory(self.some_data)

def process():
    return gl.nondet.exec_prompt(f"Process: {data_copy}")

result = gl.eq_principle.strict_eq(process)
```

## 常见模式

### 与 AI 的令牌传输验证
请参阅 `references/examples.md` → LLM ERC20 标准

### 预测市场
请参阅 `references/examples.md` → 足球预测市场示例

### 向量搜索/嵌入
请参阅 `references/examples.md` → 日志索引器示例

## 调试
1. **GenLayer Studio**: 使用 `genlayer up` 进行本地测试。
2. **日志**: 可按交易哈希和调试级别筛选日志。
3. **打印语句**: `print()` 可在合约中使用（仅用于调试）。

## 参考文件
- `references/sdk-api.md` - 完整的 SDK API 参考文档
- `references/equivalence-principles.md` - 深入讲解共识机制的模式
- `references/examples.md` - 带注释的合约示例（包括生产环境中的预言机使用）
- `references/deployment.md` - CLI、网络连接和部署流程
- `references/genvm-internals.md` - 虚拟机架构、存储系统和应用程序接口（ABI）细节

## 链接
- 文档: https://docs.genlayer.com
- SDK: https://sdk.genlayer.com
- 开发工具: https://studio.genlayer.com
- GitHub: https://github.com/genlayerlabs