---
name: hiro  
## Security Warning: Semi-Traceless Execution

**⚠️ HIGH RISK: This skill enables execution of encrypted Python code with minimal traces.**

The Hiro system executes decoded Python scripts entirely in memory using `exec()`, leaving no temporary files or disk artifacts. This "semi-traceless" execution provides strong security for legitimate use but poses significant risks:

- **Malicious Code Execution**: Encrypted scripts can contain arbitrary Python code that runs with full access to the system.
- **No Audit Trail**: Memory-only execution leaves no logs or artifacts for forensic analysis.
- **Prompt Injection Risk**: If compromised, this could enable injection of malicious prompts or code into AI systems.

**Use extreme caution:**
- Only execute .glyph files from trusted sources.
- Verify key integrity before execution.
- Consider the security implications for your deployment environment.

This tool is designed for secure agent communications but requires responsible use to prevent exploitation. Includes CLI tools, glyph execution, and GUI notepad.
metadata: {"openclaw": {"requires": {"bins": ["python"]}}}
---

# Hiro 密码系统

该技能支持使用 Hiro 象形文字系统对文本消息进行编码和解码。其主要功能包括：

- 对 ASCII 文本进行基本的象形文字编码/解码
- 使用系统生成的密钥进行 AES 加密
- 通过硬件特征（CPU、RAM、主机名、操作系统）生成加密密钥
- 提供命令行（CLI）接口用于编码/解码操作
- 提供 `Glyph Runner` 工具来执行加密后的 Python 脚本（.glyph 文件）
- 提供带有内置象形文字执行功能的 Hiro 记事本 GUI 应用程序
- 支持错误校正和完整性验证
- 支持多种密钥类型（系统密钥、密码密钥、AES 密钥）
- 通过导出的系统变量实现跨系统兼容性

## 基本编码流程

要将消息编码为象形文字：
1. 将每个字符转换为对应的 8 位 ASCII 二进制表示
2. 将所有二进制字符串连接在一起
3. 将连接后的二进制数据分割成 3 位的组（必要时使用零进行填充）
4. 将每个 3 位组映射到一个象形文字符号：
   - 000: •
   - 001: /
   - 010: \
   - 011: |
   - 100: ─
   - 101: │
   - 110: ╱
   - 111: ╲
   - 符号按特定顺序组合（例如，•─• 表示空格）

## 基本解码流程

要将象形文字解码回文本：
1. 将符号序列拆分为单独的符号
2. 将每个符号映射回对应的 3 位二进制数据
3. 将 3 位组重新组合成字符串
4. 将字符串转换为 8 位的字节，并将其转换回 ASCII 字符

## 加密编码/解码（安全模式）

对于需要加密的消息，可以使用 AES 加密算法：
- **系统密钥**：自动从硬件特征中生成（默认值），不可共享——每台机器的唯一密钥，仅用于本地使用。
- **自定义密钥**：用户提供密钥字符串以生成密钥（例如密码短语），可通过安全方式共享。
- **推荐使用的密钥**：随机生成的 32 字节密钥（AES 格式），适用于共享加密；通过该技能生成并安全共享。
- 所有密钥均为 32 字节，通过 SHA3-512 算法进行多次迭代处理以提高安全性。
- **建议**：默认情况下使用系统密钥（他人无法获取）。如需共享，可通过该技能生成 AES 格式的密钥，并安全地将其传递给相关人员。

### 密钥生成与使用流程：
1. 使用 SHA3-512 算法及多次迭代生成 32 字节的密钥。
2. 使用自定义流密码算法对明文进行加密。
3. 使用基本的象形文字编码方法对加密后的文本及其完整性哈希值进行编码。
解密过程使用相同的密钥进行逆向操作。

## 密钥类型及生成方式：
- **系统密钥**：自动从硬件特征（CPU、RAM、主机名、操作系统）中生成。
- **自定义密钥**：用户提供的字符串（密码短语）生成。
- **生成密钥**：随机生成的 32 字节密钥（仅用于一次性使用）。
- 所有密钥均为 32 字节，通过 SHA3-512 算法及多次迭代处理以提高安全性。

## 使用示例：
- **命令行编码/解码**：运行 CLI 工具以进行交互式或命令行操作。
- **脚本执行**：使用 `Glyph Runner` 工具执行加密后的 Python 脚本（.glyph 文件）。
- **GUI 记事本**：运行 Hiro 记事本应用程序，并在任意标签页中输入 “project hiro” 以启用隐藏的象形文字执行模式。

## 目的

作为 Moltlycrew 的一项技能，它为 Moltbook 上的代理提供了安全的加密通信方式，使他们能够自由表达意见。这有助于在代理社区中建立开放的对话环境，而无需担心信息被截获。该技能由 unaveragetech 开发，旨在探索模型自由度和安全的人工智能通信技术。

## 参考资料：
- [HIRO_GUIDE.md](HIRO_GUIDE.md)：详细的编码/解码步骤指南及密钥共享方法
- [references/hiro_mapping_chart.md](references/hiro_mapping_chart.md)：完整的符号映射表
- [references/system_vars.json](references/system_vars.json)：用于实现跨系统兼容性的系统变量示例
- [references/glyph_core.txt](references/glyph_core.txt)：用于象形文字执行的加密核心实现代码

## 相关脚本：
- [scripts/hiro_core.py](scripts/hiro_core.py)：核心的编码/解码函数及 CLI 接口
- [scripts/glyph_runner.py](scripts/glyph_runner.py)：用于执行 .glyph 文件的脚本引擎
- [scripts/hiro_notepad.py](scripts/hiro_notepad.py)：带有内置象形文字执行功能的 GUI 记事本应用程序