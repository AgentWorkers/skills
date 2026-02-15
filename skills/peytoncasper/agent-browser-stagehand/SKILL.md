---
name: browser
description: 通过 CLI 命令，利用自然语言自动化网页浏览器的交互操作。适用于用户需要浏览网站、导航网页、从网站中提取数据、截图、填写表单、点击按钮或与网页应用程序进行交互的场景。
allowed-tools: Bash
---

# 浏览器自动化

使用 Stagehand CLI 和 Claude 自动化浏览器操作。

### 第一步：环境选择（本地环境 vs 远程环境）

该功能会自动在本地环境和远程浏览器环境之间进行切换：
- **如果存在 Browserbase API 密钥**（.env 文件中的 BROWSERBASE_API_KEY 和 BROWSERBASE_PROJECT_ID）：使用远程 Browserbase 环境
- **如果没有 Browserbase API 密钥**：则使用本地的 Chrome 浏览器
- **无需用户提示**：根据可用配置自动选择环境

## 设置（仅首次使用）

请检查该目录下的 `setup.json` 文件。如果 `setupComplete` 的值为 `false`，则需要执行相应的设置操作：

```bash
npm install    # Install dependencies
npm link       # Create global 'browser' command
```

## 命令

所有命令在本地环境和远程环境中都具有相同的功能和用法：

```bash
browser navigate <url>                    # Go to URL
browser act "<action>"                    # Natural language action
browser extract "<instruction>" ['{}']    # Extract data (optional schema)
browser observe "<query>"                 # Discover elements
browser screenshot                        # Take screenshot
browser close                             # Close browser
```

## 快速示例

```bash
browser navigate https://example.com
browser act "click the Sign In button"
browser extract "get the page title"
browser close
```

## 环境对比

| 特性 | 本地环境 | Browserbase 环境 |
|---------|-------|-------------|
| 执行速度 | 更快 | 略慢 |
| 设置要求 | 需要安装 Chrome 浏览器 | 需要 API 密钥 |
| 隐私模式 | 不支持 | 支持 |
| 代理/验证码处理 | 不支持 | 支持 |
| 适用场景 | 开发 | 生产环境/数据抓取 |

## 最佳实践：
1. 在执行任何操作之前，先进行页面导航。
2. 每执行完一个命令后，查看截图以确认操作结果。
3. 在描述操作时请务必具体明确。
4. 操作完成后，请关闭浏览器。

## 常见问题解决方法：
- **找不到 Chrome 浏览器**：请安装 Chrome 或切换到 Browserbase 环境。
- 操作失败：使用 `browser observe` 命令查看可用的页面元素。
- Browserbase 环境出现问题：请确认 API 密钥和项目 ID 是否设置正确。

详细示例请参见 [EXAMPLES.md]。
API 参考请参见 [REFERENCE.md]。