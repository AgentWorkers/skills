# OpenClaw 的 hledger 技能

**hledger 技能** 允许 OpenClaw 代理在主机系统上执行 `hledger` 命令行界面（CLI）命令，并将结构化的输出返回给用户。  
该技能实际上是对已安装的 `hledger` 可执行文件的简单封装。

---

## 该技能的功能  
- 执行任意 `hledger` 子命令  
- 返回标准输出（stdout）和标准错误输出（stderr）  
- 支持查询账户余额、账本记录、生成报告以及访问账本数据  
- 有助于实现 OpenClaw 内部的个人财务工作流程自动化  

---

## 使用示例  
- 输入命令：`balance`  
  输出：显示默认账本文件中的账户余额。  
- 输入命令：`register Assets`  
  输出：显示 `Assets` 账户的注册记录。  
- 输入命令：`balance -f myledger.journal`  
  输出：使用指定的账本文件运行 `hledger` 命令。  

---

## 使用要求  
- 确保已安装 `hledger`，并且该程序在系统的 `PATH` 环境变量中可被找到。  
- 用户必须具有对其账本文件的读取权限。  
- 可通过运行 `hledger --version` 来测试 `hledger` 是否已正确安装。  

---

## 安全注意事项  
- 该技能通过本地 `hledger` 可执行文件来执行 shell 命令；仅允许执行 `hledger` 相关的命令，不允许执行任意其他 shell 命令。  

---

## 预期用途  
- 个人财务自动化处理  
- 通过聊天界面查询账本信息  
- 与基于 OpenClaw 的 Telegram 或 WhatsApp 机器人集成  
- 财务报告流程的自动化  

---

## 版本信息  
1.0.0