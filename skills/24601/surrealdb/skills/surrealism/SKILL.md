---
name: surrealism
description: "SurrealDB 的 Surrealism WASM 扩展开发：编写 Rust 函数，将其编译为 WASM 文件，然后作为数据库模块进行部署。这是 surreal-skills 组件的一部分。"
license: MIT
metadata:
  version: "1.0.2"
  author: "24601"
  parent_skill: "surrealdb"
  snapshot_date: "2026-02-19"
  upstream:
    repo: "surrealdb/surrealdb"
    release: "v3.0.0"
    sha: "2e0a61fd4daf"
    docs: "https://surrealdb.com/docs/surrealdb/extensions"
---
# 超现实主义（Surrealism）——SurrealDB的WASM扩展

SurrealDB 3.0的新特性：允许用户使用Rust语言编写自定义函数，将其编译为WebAssembly（WASM）代码，然后作为原生数据库模块部署，从而可以通过SurrealQL直接调用这些函数。

## 先决条件

- 安装了支持`wasm32-unknown-unknown`目标的Rust工具链
- 使用SurrealDB CLI v3.0.0或更高版本（包含`surreal module`子命令的`surreal`二进制文件）
- 熟悉SurrealQL中的`DEFINE MODULE`和`DEFINE BUCKET`命令

## 开发工作流程

```
1. Annotate   -- surrealism.toml + #[surrealism] on Rust functions
2. Compile    -- surreal module compile  (produces .wasm binary)
3. Register   -- DEFINE BUCKET + DEFINE MODULE in SurrealQL
```

## 快速入门

```bash
# Create a new Surrealism project
cargo new --lib my_extension
cd my_extension

# Add the WASM target
rustup target add wasm32-unknown-unknown

# Create surrealism.toml (required manifest)
cat > surrealism.toml << 'TOML'
[package]
name = "my_extension"
version = "0.1.0"
TOML

# Write your extension (annotate with #[surrealism])
cat > src/lib.rs << 'RUST'
use surrealism::surrealism;

#[surrealism]
fn greet(name: String) -> String {
    format!("Hello, {}!", name)
}
RUST

# Compile to WASM using SurrealDB CLI
surreal module compile

# Register in SurrealDB
surreal sql --endpoint http://localhost:8000 --user root --pass root --ns test --db test
```

```surql
-- Grant access to the WASM file
DEFINE BUCKET my_bucket;

-- Register the module functions
DEFINE MODULE my_extension FROM 'my_bucket:my_extension.wasm';

-- Use the function in queries
SELECT my_extension::greet('World');
```

## 使用场景

- 通过SurrealQL调用自定义的标量函数
- 生成用于测试的虚拟数据
- 实现特定领域的逻辑（如语言处理、量化金融、自定义编码）
- 使用Rust库中的特定功能（这些功能在SurrealDB核心库中不可用）
- 开发用于全文搜索的自定义分析工具

## 状态

Surrealism功能仍处于开发阶段，尚未稳定。在SurrealDB 3.x版本发布期间，API可能会发生变化。如有任何反馈，请通过GitHub的issue或PR提交到[surrealdb/surrealdb](https://github.com/surrealdb/surrealdb)仓库。

## 完整文档

请参阅以下文档以获取详细信息：

- **[rules/surrealism.md](../../rules/surrealism.md)**：项目设置、Rust函数签名、WASM编译、`DEFINE MODULE/BUCKET`语法、部署、测试及最佳实践
- **[SurrealDB扩展文档](https://surrealdb.com/docs/surrealdb/extensions)**：官方扩展文档
- **[CLI模块命令参考](https://surrealdb.com/docs/surrealdb/cli/module)**：`surreal module`命令的使用说明