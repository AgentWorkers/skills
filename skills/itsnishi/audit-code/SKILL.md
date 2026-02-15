---
name: audit-code
description: 以安全性为重点的代码审查，针对硬编码的秘密信息、危险的函数调用以及常见的安全漏洞
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
context: fork
---

# audit-code -- 项目代码安全审查

针对项目源代码的安全性审查，重点检查OWASP风格的漏洞、硬编码的敏感信息、危险的功能调用以及与人工智能辅助开发相关的安全问题。

## 使用方法

将审计工具运行在目标路径上：

```bash
python3 "$SKILL_DIR/scripts/audit_code.py" "$ARGUMENTS"
```

如果 `$ARGUMENTS` 为空，则默认使用 `$PROJECT_ROOT`。

## 审查内容：

- **硬编码的敏感信息**：API密钥（AWS、GitHub、Stripe、OpenAI、Slack）、令牌、私钥、连接字符串、密码等
- **危险的功能调用**：`eval`、`exec`、`subprocess`（设置 `shell=True`）、`child_process.exec`、`pickle` 解序列化、`system()`、`gets()` 等
- **SQL注入**：SQL查询中的字符串拼接/插入操作
- **依赖风险**：使用已知存在问题的软件包、未经验证的依赖库
- **敏感文件**：提交到 Git 的 `.env` 文件、仓库中的凭证文件
- **文件权限**：过于宽松的文件权限设置
- **数据泄露风险**：通过 Base64 编码后通过网络传输数据、DNS 欺骗、读取凭证文件等方式进行数据泄露

## 输出结果

生成结构化的报告，其中包含按严重程度排序的发现结果、文件位置以及可执行的修复步骤。

## 使用场景：

- 在提交或推送代码之前
- 在审查第三方贡献或 Pull Request 时
- 作为代码库定期安全审计的一部分
- 在使用人工智能辅助生成代码后，验证是否引入了新的敏感信息或安全漏洞