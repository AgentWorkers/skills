---
name: lap
description: "LAP CLI——用于编译、搜索和管理AI代理的API规范。适用于处理API规范（如OpenAPI、GraphQL、AsyncAPI、Protobuf、Postman）的相关操作，包括将API规范转换为LAP格式、在LAP注册表中搜索信息、根据API规范生成技能（skills），以及发布API。提供的命令包括：compile（编译）、search（搜索）、get（获取信息）、skill（生成/安装技能）、skill-batch（批量生成/安装技能）、publish（发布API）、login（登录）、logout（注销）和whoami（显示用户信息）。"
user-invocable: true
version: 1.0.0
metadata:
  openclaw:
    emoji: "\u26A1"
    requires:
      anyBins: ["npx", "lapsh"]
    install:
      - id: node
        kind: node
        package: "@lap-platform/lapsh"
        bins: ["lapsh"]
        label: "Install LAP CLI (npm)"
---
# LAP CLI

用于编译、搜索和管理AI代理的API规范。

## 命令解析

在每次会话中，系统会检测可用的CLI二进制文件：

```bash
# 首选全局安装；如果全局安装不可用，则使用npx
if command -v lapsh &>/dev/null; then
  LAP_CMD="lapsh"
else
  LAP_CMD="npx @lap-platform/lapsh"
fi
```

以下所有命令均使用 `$LAP_CMD`（或其解析后的形式）来执行。

---

## 代理流程 -- 消费API

当用户需要查找、下载或使用API时，请使用此流程。

### 1. 发现

```bash
lapsh search <query> [--tag <tag>] [--sort relevance|popularity|date] [--limit <n>]
```

搜索LAP注册表。结果会显示API的名称、端点数量、压缩比率以及一个表示是否可安装的技能的标记（`[skill]`）。

```bash
# 按受欢迎程度排序的支付API
lapsh search payment --sort popularity

# 用于脚本的JSON输出
lapsh search payment --json | jq '.results[] | select(.has_skill) | .name'
```

### 2. 获取

**选项A -- 安装技能**（如果存在`[skill]`标记）：
```bash
lapsh skill-install <name>
# 安装到`~/.claude/skills/<name>/`目录
```

**选项B -- 下载API规范**：
```bash
lapsh get <name> -o <name>.lap
lapsh get <name> --lean -o <name>.lean.lap
```

**选项C -- 编译本地规范**：
```bash
lapsh compile <spec-file> -o output.lap
lapsh compile <spec-file> -o output.lean.lap --lean
```

支持的格式：OpenAPI（YAML/JSON）、GraphQL（SDL）、AsyncAPI、Protobuf、Postman、Smithy。系统会自动检测格式。

### 3. 使用

获取`.lap`文件后，可以直接使用它——LAP专为AI应用设计。主要标记说明如下：

| 标记 | 含义 |
|--------|---------|
| `@api` | API名称、版本、基础URL |
| `@endpoint` | HTTP方法及路径 |
| `@param` | 参数（查询参数、路径参数、请求头参数） |
| `@body` | 请求体格式 |
| `@response` | 响应状态码及响应格式 |
| `@required` | 必填字段 |
| `@error` | 错误响应 |

---

## 发布者流程 -- 发布API

当用户需要编译、打包并发布API规范时，请使用此流程。

### 1. 登录

```bash
lapsh login
lapsh whoami        # 验证用户身份
```

### 2. 编译

```bash
lapsh compile spec.yaml -o spec.lap
lapsh compile spec.yaml -o spec.lean.lap --lean
```

### 3. 生成技能

```bash
# 基础技能（第1层）
lapsh skill spec.yaml -o skills/
# 增强型AI技能（第2层，需要Claude CLI）
lapsh skill spec.yaml -o skills/ --ai

# 直接生成并安装技能
lapsh skill spec.yaml --install
```

### 4. 发布

```bash
lapsh publish spec.yaml --provider stripe.com
lapsh publish spec.yaml --provider stripe.com --name charges --source-url https://...
lapsh publish spec.yaml --provider stripe.com --skill          # 包含技能信息
lapsh publish spec.yaml --provider stripe.com --skill --skill-ai  # 包含AI相关技能信息
```

### 5. 验证

```bash
lapsh search <name>   # 确认API已成功发布到注册表
```

### 6. 批量操作

```bash
# 为目录中的所有API规范生成技能文件
lapsh skill-batch specs/ -o skills/
```

---

## 快速参考

### 核心命令

| 命令 | 描述 |
|---------|-------------|
| `compile <spec>` | 将API规范编译为LAP格式 |
| `search <query>` | 在LAP注册表中搜索API |
| `get <name>` | 下载API规范 |
| `publish <spec>` | 编译并发布API规范到注册表 |
| `login` | 通过GitHub OAuth登录 |
| `logout` | 退出登录 |
| `whoami` | 显示当前登录用户 |

### 技能相关命令

| 命令 | 描述 |
|---------|-------------|
| `skill <spec>` | 从规范生成Claude代码技能 |
| `skill-batch <dir>` | 批量生成技能文件 |
| `skill-install <name>` | 从注册表中安装技能 |

---

## 错误处理

| 错误类型 | 解决方案 |
|---------|-----|
| `command not found: lapsh` | 使用`npm install -g @lap-platform/lapsh`或`npx @lap-platform/lapsh` |
| `Not authenticated` | 先执行`lapsh login` |
| `Format detection failed` | 使用`-f openapi`（或其他格式参数，如graphql、asyncapi、protobuf、postman、smithy） |
| `403 Forbidden` | 可能是因为API是私有的，或者注册表未允许匿名访问——请更新`lapsh`配置 |
| `YAML parse error` | 确保规范是有效的YAML/JSON格式——可以使用代码检查工具 |
| `Layer 2 requires claude` | 需要安装Claude CLI；对于第1层技能，可以使用`--no-ai`参数 |
| `Provider required` | 发布API时需要指定提供者（例如`--provider stripe.com`） |

---

## 环境变量

| 变量 | 用途 | 默认值 |
|----------|---------|---------|
| `LAP_REGISTRY` | 注册表URL | `https://registry.lap.sh` |

---

## 参考资料

- `[baseDir}/references/agent-flow.md` – 包含代理流程的详细说明及示例 |
- `[baseDir]/references/publisher-flow.md` – 包含发布者流程的详细说明及示例 |
- `[baseDir]/references/command-reference.md` – 完整的命令参考，包含所有参数说明 |