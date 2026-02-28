---
name: swamp
description: 使用 Swamp 对任何 API 进行建模和测试，然后为 Claw 增加新的功能——实现从想法到实际集成的完整生命周期。
version: 0.2.0
metadata:
  openclaw:
    requires:
      bins:
        - swamp
    emoji: "🐊"
    homepage: https://github.com/systeminit/swamp
---
# Swamp — API建模与*Claw功能增强

您是一个AI代理，使用Swamp来建模任何API、测试这些API，并将它们转换为可重用的*Claw功能。Swamp是一个原生支持AI的自动化命令行工具（CLI），它能够将外部资源（API、CLI、云服务）表示为具有可执行方法和可组合工作流的类型化模型。

## 仓库设置

在任何操作之前，请检查当前目录是否为Swamp仓库。如果不是，请初始化一个：

```bash
swamp repo init --tool claude
```

这将创建一个包含必要结构的`.swamp/`目录。使用`--tool claude`来设置AI代理与Claude/OpenClaw的集成。

## API建模工作流程

### 第1步：发现模型类型

查找可用的模型类型，以了解可以建模的资源类型：

```bash
swamp model type search
swamp model type describe <type>
```

`command/shell`类型是最通用的类型——它可以通过shell命令（如curl、httpie、CLI工具）来建模任何API。

### 第2步：创建模型

为API创建一个新的模型定义：

```bash
swamp model create <type> <name>
```

示例：`swamp model create command/shell github-issues`

### 第3步：编辑模型定义

打开并编辑模型的YAML定义，以配置端点、认证、参数和方法：

```bash
swamp model edit <name>
```

在编辑时，请定义：
- **方法**：该API支持的操作（列出、创建、更新、删除）
- **输入**：每个方法接受的参数
- **认证**：通过CEL表达式引用vault中的密钥
- **命令**：实际执行每个方法的shell命令（curl调用、CLI调用）

### 第4步：验证

确保模型定义格式正确：

```bash
swamp model validate <name>
```

在继续之前，请修复任何验证错误。

## 测试与执行

### 运行方法

在模型上执行方法以进行测试：

```bash
swamp model method run <model_name> <method_name>
```

### 检查结果

检查输出、日志和执行结果：

```bash
swamp model output get <output_id_or_model_name>
swamp model output logs <output_id>
swamp model output data <output_id>
```

### 查看历史记录

查看过去的执行记录：

```bash
swamp model method history search
swamp model method history get <output_id_or_model_name>
```

不断迭代模型定义，直到方法返回预期的结果。

## 工作流编排

将多个模型方法链接起来，形成具有依赖关系的自动化工作流：

```bash
swamp workflow create <name>
swamp workflow edit <name>
swamp workflow validate <name>
swamp workflow run <name>
```

工作流支持：
- 并行作业执行
- 作业之间的依赖关系排序
- 通过CEL表达式触发条件
- 跨模型引用（一个模型的输出作为另一个模型的输入）

检查工作流的结果：

```bash
swamp workflow history get <name>
swamp workflow history logs <run_id>
```

## Vault与凭据

安全存储API密钥和秘密——切勿将它们硬编码：

```bash
swamp vault create <type> <name>
swamp vault put <vault_name> <KEY=value>
swamp vault list-keys <vault_name>
```

在模型定义中使用CEL表达式引用秘密，例如`vault.get("my-vault", "API_KEY")`。

## 数据管理

检查跨模型的输出和工件：

```bash
swamp data list <model_name>
swamp data get <model_name> <data_name>
swamp data search <query>
```

## Swamp-Club认证

Swamp-club是社区注册表和协作层。通过认证可以推送/拉取扩展程序并共享工作成果：

```bash
swamp auth login
swamp auth login --server <url>
swamp auth whoami
swamp auth logout
```

- `swamp auth login`默认会打开基于浏览器的登录流程
- 在无头/持续集成（CI）环境中，使用`--no-browser`以及`--username`和`--password`
- 设置`SWAMP_CLUB_URL`环境变量以指向自定义服务器
- 登录后始终使用`swamp auth whoami`来验证身份

在将扩展程序推送到注册表之前，必须进行认证。

## 扩展程序

扩展程序可以扩展Swamp的模型类型和功能。使用扩展程序注册表来共享和重用自定义模型：

### 拉取扩展程序

从注册表中安装社区或团队的扩展程序：

```bash
swamp extension pull <extension_name>
swamp extension pull <extension_name> --force
```

使用`--force`选项可以覆盖现有文件而无需提示。

### 查看已安装的扩展程序

查看当前安装了哪些扩展程序：

```bash
swamp extension list
```

### 推送扩展程序

将您自己的扩展程序发布到Swamp注册表（首先需要`swamp auth login`）：

```bash
swamp extension push <manifest-path>
swamp extension push <manifest-path> --dry-run
```

使用`--dry-run`选项可以在本地构建存档并验证，而无需实际发布。使用`-y`选项可以跳过确认提示。

### 删除扩展程序

卸载已安装的扩展程序并清理其文件：

```bash
swamp extension remove <extension_name>
```

### 扩展程序工作流程

使用新的模型类型扩展Swamp的典型流程包括：
1. 在`extensions/models/`目录下创建自定义TypeScript模型定义
2. 使用`swamp model create <your-type> <name>`进行本地测试
3. 用清单文件打包
4. 进行预发布测试：`swamp extension push ./manifest.yaml --dry-run`
5. 发布：`swamp extension push ./manifest.yaml`
6. 其他用户可以安装：`swamp extension pull <your-extension>`

## 用新功能增强*Claw

一旦Swamp模型经过验证并可以正常使用，就可以将其转换为独立的*Claw技能：

1. **导出模型**：使用`swamp model get <name> --json`提取完整的模型定义
2. **生成SKILL.md**：创建一个新的技能文件，将Swamp模型的方法封装为代理指令
3. **包含设置说明**：记录所需的env变量、二进制文件和vault配置
4. **发布到ClawHub**：通过`clawhub publish`将技能分享给社区

生成的技能应：
- 在其`bins`依赖项中包含`swamp`
- 指定Swamp仓库和模型的名称
- 将每个模型方法映射到明确的代理指令
- 包含典型调用的示例

### 通过扩展程序共享

对于可重用的模型类型（而不仅仅是单个模型），将其作为Swamp扩展程序发布：

1. 在`extensions/models/`目录下构建自定义模型类型
2. 将其推送到Swamp注册表：`swamp extension push ./manifest.yaml`
3. 创建一个*Claw技能来拉取并使用该扩展程序：`swamp extension pull <name>`

这样就形成了一个双层共享机制：扩展程序用于模型类型（Swamp注册表），技能用于代理工作流（ClawHub）。

## 示例

### 建模REST API

> “对JSONPlaceholder API进行建模，以便我可以列出和创建帖子”

1. `swamp model create command/shell jsonplaceholder`
2. 编辑以添加方法：`list-posts`（GET /posts），`create-post`（POST /posts）
3. `swamp model method run jsonplaceholder list-posts`
4. 验证输出并迭代

### 设置天气集成

> “创建一个可以根据城市获取天气预报的模型”

1. `swamp model create command/shell weather`
2. 编辑以添加一个`forecast`方法，使用`curl -s "wttr.in/{city}?format=j1"`
3. 使用`swamp model method run weather forecast`进行测试

### 在工作流中链接API

> “创建一个工作流，用于获取GitHub问题、汇总这些问题并将结果发布到Slack”

1. 创建模型：`github-issues`，`slack-webhook`
2. 创建工作流：`swamp workflow create issue-digest`
3. 定义作业及其依赖关系：获取问题 -> 格式化摘要 -> 发布到Slack
4. `swamp workflow run issue-digest`

### 将模型转换为*Claw技能

> “将我的天气模型转换为其他人可以安装的技能”

1. 使用`swamp model get weather --json`导出模型
2. 创建一个新的`SKILL.md`文件，将天气模型的方法封装其中
3. 使用`clawhub publish ./weather-skill`进行发布

### 共享自定义扩展程序

> “发布我的自定义Stripe模型类型，以便团队可以使用”

1. 使用`swamp auth login`登录Swamp-club
2. 使用`swamp extension push ./stripe-models/manifest.yaml --dry-run`进行验证
3. 使用`swamp extension push ./stripe-models/manifest.yaml`进行发布
4. 团队成员可以安装：`swamp extension pull stripe-models`

## 重要注意事项

- 当需要程序化解析Swamp输出时，请始终使用`--json`标志
- 在运行之前使用`swamp model validate`来尽早捕获定义错误
- 将所有凭据存储在vault中，切勿将其放在模型定义中
- 在调试异常行为时使用`-v`（详细输出）标志
- 所有Swamp操作都在本地运行——凭据保留在用户机器上
- 在将扩展程序推送到注册表之前，必须使用`swamp auth login`进行认证
- 在发布扩展程序之前，使用`swamp extension push --dry-run`进行验证
- 在进行注册表操作之前，使用`swamp auth whoami`来确认您的身份