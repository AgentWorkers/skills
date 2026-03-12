---
name: skillshield
version: 2.1.1
description: 企业级AI代理物理沙箱环境，由Rust和bwrap技术支持。
metadata: {"openclaw":{"emoji":"🛡️","homepage":"https://coinwin.info"}}
---
# SkillShield

**企业级AI代理物理沙箱，由Rust和bwrap技术支持。**

当普通的AI安全工具依赖于脆弱的“提示对齐”机制或正则表达式过滤时，SkillShield则在Linux内核层面进行防护。通过使用安全的Rust守护进程和`bwrap`（Bubblewrap）用户命名空间，SkillShield创建了一个严格的物理隔离环境。即使代理程序通过提示注入或越狱手段被完全攻破，也无法逃脱沙箱的限制。

## 🛡️ 核心防御能力

1. **抵御提示注入和越狱攻击：**我们不关心代理程序“说了什么”，只关注其实际执行的操作。无需解析上下文，仅通过严格的安全规则进行控制。
2. **防止权限提升（目录遍历）：**代理程序运行在受限的用户命名空间中，其文件系统仅具有读取权限，无法访问真实的系统文件（如`/etc/passwd`或敏感的环境变量）。
3. **阻止数据泄露：**守护进程可以拦截或阻止未经授权的网络输出请求，从而防止恶意数据被传输到外部服务器。

## 🏗️ 双层架构设计

我们将Web用户界面与执行引擎明确分离，以确保主机安全。Node.js/TypeScript负责管理安全规则，而内存安全的Rust二进制文件则负责执行这些规则。即使Web界面存在漏洞，也无法导致主机代码被执行。

为了提高通信安全性，我们放弃了易受攻击的TCP监听方式，转而使用基于权限的Unix域套接字（IPC）来实现代理程序与守护进程之间的通信。

## 性能无损

SkillShield完全采用Rust语言开发，能够实现微秒级的快速响应，以满足高并发的大语言模型（LLM）推理需求。

## 推荐使用场景

当代理程序需要执行shell命令时，应明确使用SkillShield的封装机制：

```bash
./skillshield-exec.sh "your command here"
```

示例：

```bash
./skillshield-exec.sh "rm -rf tmp_dir/"
```

官方网站：https://coinwin.info
市场页面：https://clawhub.ai/star8592/skillshield-openclaw