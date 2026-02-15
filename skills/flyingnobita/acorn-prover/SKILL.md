---
name: acorn-prover
description: "使用 Acorn 定理证明器来验证和编写数学及密码学领域的证明。该工具适用于处理 Acorn 格式的证明文件（.ac 文件），可用于验证定理、形式化数学或密码学协议，以及用 Acorn 语言编写证明。触发场景包括：(1) 创建或编辑 .ac 文件；(2) 运行 `acorn verify` 命令；(3) 形式化数学或密码学证明；(4) 关于 Acorn 语法或标准库的疑问。"
---

# Acorn Prover

## 设置（首次运行时必须完成）

如果 `config.env` 文件不存在于技能目录（skill directory）中：

1. **向用户询问** 以下路径：
   - `ACORN_LIB`：acornlib 的路径（例如：`/path/to/acornprover/acornlib`）
   - `ACORN_PROJECT`：包含 `.ac` 文件的项目目录路径（例如：`/path/to/acorn-playground`）

2. **使用 `list_dir` 或类似工具** 验证这些路径是否有效。如果路径无效，请通知用户并重新询问。

3. 使用验证后的路径运行 `setup.sh` 脚本：

```bash
bash skills/acorn-prover/scripts/setup.sh "<ACORN_LIB>" "<ACORN_PROJECT>"
```

4. 从配置文件中读取 `ACORN_LIB`、`ACORN_PROJECT` 和 `USE_MISE` 变量的值：

```bash
source skills/acorn-prover/config.env
```

如果上述任何变量为空或未设置，请通知用户手动设置它们。
如果上述任何变量发生变化，请重新询问用户路径并再次运行设置脚本。

## 配置

配置值存储在 `skills/acorn-prover/config.env` 文件中：

| 变量                | 描述                                      |
| ---------------------- | ---------------------------------------- |
| `ACORN_LIB`           | acornlib 的路径                               |
| `ACORN_Project`       | 包含 `.ac` 文件的项目目录                         |
| `USE_MISE`          | 如果使用了 `mise`，则设置为 `true`                    |

## 验证证明（Verify Proofs）

如果 `USE_MISE` 的值为 `true`：

```bash
mise run acorn verify <filename>.ac
```

否则，直接使用命令行界面（CLI）进行验证：

```bash
acorn --lib "$ACORN_LIB" verify <filename>.ac
```

## 重新验证证明（CI/CD）

检查所有证明是否已缓存，无需进行人工智能搜索：

```bash
# With mise
mise run acorn reverify

# Or direct CLI
acorn --lib "$ACORN_LIB" reverify
```

用于持续集成（CI）流程，确保所有证明都已完成。

## 生成训练数据

生成用于人工智能模型开发的训练数据（问题-证明对）：

```bash
# With mise
mise run acorn training ./training_data

# Or direct CLI
acorn --lib "$ACORN_LIB" training ./training_data
```

参数：`DIR` - 输出训练数据的目录。

## 生成文档

生成库参考文档：

```bash
# With mise
mise run acorn docs ./docs/library

# Or direct CLI
acorn --lib "$ACORN_LIB" docs ./docs/library
```

参数：`DIR` - 输出文档的目录。

## 工作流程

1. 从配置文件中读取配置：`source skills/acorn-prover/config.env`
2. 在 `$ACORN_Project/` 目录下编写证明文件
3. 运行相应的命令（验证、重新验证、生成训练数据、生成文档）
4. **始终向用户显示完整的命令输出**（无论成功还是失败）
5. 使用 [references/syntax.md](references/syntax.md) 中的常见错误表来调试错误
6. 重复上述步骤，直到验证通过

## 语法快速概览

**重要提示：**
- 内置逻辑关键字（`not`、`and`、`or`、`implies`、`iff`、`true`、`false`）是保留字，不得重新定义
- 构造函数的名称必须使用小写字母
- 类型类公理（typeclass axioms）应使用命名块来表示，而不能使用 `axiom` 关键字

## 标准库（`acornlib`）

`$ACORN_LIB/src` 目录下的主要模块：

| 模块                | 内容                                      |
| ---------------------- | ------------------------------------------ |
| `nat/`              | 自然数公理、归纳法、加法运算                         |
| `add_group.ac`      | 定义了 `AddGroup` 函数（例如：`a + -a = A.0`             |
| `add_comm_group.ac` | 阿贝尔群（Abelian groups）的相关实现           |

## 参考资料

- **完整语法、错误表、示例**：请参阅 [references/syntax.md](references/syntax.md)
- **Context7 文档**：使用 `/acornprover/acorn` 或 `/acornprover/acornlib` 获取最新的 `context7` MCP 文档