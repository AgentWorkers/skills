---
name: surrealism
description: "SurrealDB的Surrealism WASM扩展开发：编写Rust函数，将其编译为WASM格式，然后作为数据库模块进行部署。这是surreal-skills系列的一部分。"
license: MIT
metadata:
  version: "1.0.4"
  author: "24601"
  parent_skill: "surrealdb"
  snapshot_date: "2026-02-19"
  upstream:
    repo: "surrealdb/surrealdb"
    release: "v3.0.0"
    sha: "2e0a61fd4daf"
    docs: "https://surrealdb.com/docs/surrealdb/extensions"
---
# 超现实主义（Surrealism）——SurrealDB的WASM扩展功能

**SurrealDB 3.0的新特性：**  
您可以使用Rust语言编写自定义函数，将其编译为WebAssembly（WASM），并作为原生数据库模块部署，从而在SurrealQL中直接调用这些函数。

## 先决条件：  
- 安装了支持`wasm32-unknown-unknown`目标的Rust工具链（稳定版本）  
- 使用SurrealDB CLI v3.0.0或更高版本（`surreal`二进制文件及`surreal module`子命令）  
- 熟悉SurrealQL中的`DEFINE MODULE`和`DEFINE BUCKET`命令语法  

## 开发流程：  
（具体开发步骤请参见下面的代码块说明。）  

## 快速入门：  
（快速开始使用WASM扩展功能的步骤，请参见下面的代码块。）  

## 使用场景：  
- 在SurrealQL中调用自定义标量函数  
- 生成用于测试的虚拟数据  
- 实现特定领域的逻辑（如语言处理、量化金融、自定义编码）  
- 使用SurrealDB核心功能无法满足的特殊用例（例如，特定Rust库的功能）  
- 开发用于全文搜索的自定义分析工具  

## 状态：  
Surrealism功能仍处于开发阶段，尚未稳定。在SurrealDB 3.x版本更新期间，API可能会发生变化。  
如有任何反馈或建议，请通过GitHub问题或Pull Request提交到[surrealdb/surrealdb](https://github.com/surrealdb/surrealdb)仓库。  

## 完整文档：  
有关详细的使用指南，请参阅以下文档：  
- **[rules/surrealism.md](../../rules/surrealism.md)**：项目设置、Rust函数签名、WASM编译、`DEFINE MODULE/BUCKET`语法、部署、测试及最佳实践  
- **[SurrealDB扩展文档](https://surrealdb.com/docs/surrealdb/extensions)**：官方扩展文档  
- **[CLI模块命令参考](https://surrealdb.com/docs/surrealdb/cli/module)**：`surreal module`命令的使用说明