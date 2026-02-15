---
name: browserbase-fix
description: **指导 Claude 进行调试并修复失败的浏览器自动化脚本**

**一、调试流程：**

1. **观察错误日志**：首先仔细阅读浏览器控制台（Console）中输出的错误信息。这些信息通常会指出自动化脚本执行过程中遇到的问题所在。

2. **检查代码逻辑**：根据错误日志，逐一检查相关代码段，找出可能导致问题的逻辑错误或语法错误。

3. **使用调试工具**：许多浏览器提供了内置的调试工具（如 Chrome 的开发者工具），可以帮助你逐步执行自动化脚本，观察每一步的执行结果，从而更容易定位问题。

4. **添加日志记录**：在代码中添加适当的日志记录语句，以便在调试过程中更好地了解脚本的执行状态和变量值。

5. **逐步缩小问题范围**：通过逐步缩小问题发生的范围（例如，仅测试特定的功能或条件），逐步定位问题的根本原因。

6. **修复错误并重新测试**：修复找到的错误后，重新运行自动化脚本，确保问题已经得到解决。

**二、常见错误及解决方法：**

1. **语法错误**：检查代码中是否存在拼写错误、括号不匹配等问题。使用代码编辑器的代码检查功能或语法检查工具可以帮助你发现这类错误。

2. **逻辑错误**：确保自动化脚本的逻辑符合预期的行为。例如，条件判断是否正确、循环是否正常执行等。

3. **浏览器兼容性问题**：不同的浏览器可能对自动化脚本有不同的支持程度。尝试在不同的浏览器上运行脚本，以检查是否存在兼容性问题。

4. **网络请求问题**：如果脚本依赖于网络请求（如 AJAX），请确保请求的 URL 正确、请求头设置正确，并检查是否能够成功获取到数据。

5. **超时问题**：如果脚本在等待网络响应时超时，检查请求的超时设置是否合理，并考虑增加超时时间。

6. **性能问题**：如果脚本运行缓慢，可能是由于代码效率低下或资源消耗过大导致的。优化代码或减少不必要的操作可以提高性能。

**三、示例：**

假设你有一个自动化脚本，用于在浏览器中点击某个链接并检查页面是否加载完成。如果脚本在执行过程中遇到错误，你可以按照以下步骤进行调试：

```markdown
# 示例：调试失败的浏览器自动化脚本

# 1. 观察错误日志
打开浏览器控制台，查找与脚本执行相关的错误信息。

# 2. 检查代码逻辑
找到错误信息对应的代码段，检查是否有逻辑错误或语法错误。

# 3. 使用调试工具
在 Chrome 开发者工具中，逐步执行脚本，观察每一步的执行结果。例如，使用“Step into”（步入）功能逐行执行代码，查看变量值的变化。

# 4. 添加日志记录
在脚本中添加如下日志记录语句：
```javascript
console.log('当前执行的步骤:', stepNumber);
```
这可以帮助你了解脚本的执行流程。

# 5. 逐步缩小问题范围
尝试仅测试脚本中的某个特定功能或条件，以缩小问题范围。

# 6. 修复错误并重新测试
修复错误后，重新运行脚本，确保问题已经得到解决。

**四、总结：**

调试和修复失败的浏览器自动化脚本需要耐心和细致。通过观察错误日志、检查代码逻辑、使用调试工具以及逐步缩小问题范围，你可以逐步找到并解决问题。同时，保持良好的代码质量和注释习惯也有助于提高脚本的稳定性和可维护性。
---

# 修复自动化技能

本技能指导用户如何调试和修复失败的浏览器自动化脚本。

## 使用场景

在以下情况下使用本技能：
- 当 Browserbase 的某个功能在生产环境中出现故障时；
- 当自动化脚本停止运行时（可能是由于网站结构发生变化）；
- 当用户报告自动化脚本出现错误时；
- 当与浏览器功能相关的 CI/CD 流程出现故障时。

## 诊断信息来源

在开始调试之前，需要收集以下信息：
1. **错误信息**：用户报告的错误内容或 CI 日志中的详细信息；
2. **功能代码**：自动化脚本的源代码；
3. **最近的执行记录**：分析故障发生的规律；
4. **功能的使用历史**：最后一次正常运行的时间是什么时候？

```bash
stagehand fn errors <function-name>
stagehand fn logs <function-name>
```

## 调试流程

### 1. 重现问题

启动一个 Browserbase 会话以查看问题所在：
```bash
stagehand session create
stagehand session live  # Open in browser to watch
```

导航到目标 URL：
```bash
stagehand goto <target-url>
```

### 2. 对比预期状态与实际状态

获取当前页面的快照：
```bash
stagehand snapshot
```

与自动化脚本的预期结果进行对比：
- 预期的元素是否存在？
- 选择器是否发生了变化？
- 是否出现了登录限制或验证码？
- 页面结构是否发生了变化？

### 3. 常见故障类型

#### 选择器变化
网站更新了 HTML 结构：
```bash
stagehand snapshot
# Look for similar elements with new selectors
stagehand eval "document.querySelector('.new-class')?.textContent"
```

**解决方法**：更新自动化脚本中的选择器。

#### 时间问题
元素加载速度比预期慢：
```bash
stagehand network on
stagehand goto <url>
stagehand network list
# Check if resources are slow to load
```

**解决方法**：添加显式的等待时间或增加超时设置。

#### 认证失效
会话 cookie 失效：
```bash
stagehand snapshot
# Look for login prompts
```

**解决方法**：重新进行认证或更新认证流程。请参考 `skills/auth/SKILL.md`。

#### 速率限制/机器人检测
网站阻止自动化访问：
```bash
stagehand network list
# Look for 403, 429 status codes
stagehand screenshot -o blocked.png
```

**解决方法**：添加延迟、使用代理服务器或联系网站管理员。

#### 网站重新设计
网站结构发生了重大变化：
```bash
stagehand snapshot
stagehand screenshot -o current.png
```

**解决方法**：重新编写受影响的自动化脚本部分。

### 4. 测试修复结果

对功能代码进行修改后，进行测试：
```bash
# Test locally first
stagehand fn invoke <name> --local

# If local works, deploy
stagehand fn publish <entrypoint>

# Test in production
stagehand fn invoke <name>
```

### 5. 验证修复是否完成

修复完成后：
1. 多次运行该功能以确保其稳定性；
2. 检查是否返回了所有预期的数据；
3. 验证边缘情况是否仍然能够正常处理。

## 提交和部署

修复完成后，使用 git 提交更改：
```bash
git add <function-file>
git commit -m "fix(<function-name>): <description of fix>"
git push
```

如果这是 PR 流程：
```bash
gh pr create --title "Fix <function-name>" --body "..."
```

## 诊断命令参考

| 命令 | 用途 |
|---------|---------|
| `stagehand session create` | 启动调试会话 |
| `stagehand session live` | 打开可视化调试工具 |
| `stagehand goto <url>` | 导航到目标地址 |
| `stagehand snapshot` | 检查 DOM 结构 |
| `stagehand screenshot` | 拍摄页面截图 |
| `stagehand network on` | 启用请求捕获功能 |
| `stagehand network list` | 查看捕获的请求记录 |
| `stagehand network show <id>` | 查看特定请求的详细信息 |
| `stagehand eval <js>` | 运行诊断用 JavaScript 代码 |
| `stagehand fn errors <name>` | 查看最近发生的错误 |
| `stagehand fn logs <name>` | 查看函数日志 |

## 调试会话示例
```
User: My price-monitor function stopped working yesterday

Claude: Let me investigate. First, let me check the recent errors:

> stagehand fn errors price-monitor

I see several failures with "Element not found: .price". Let me start a debug session:

> stagehand session create
> stagehand session live
> stagehand goto https://example.com/product/123

Opening in browser so you can watch. Let me check the page structure:

> stagehand snapshot

I can see the price element now uses a different class `.product-price` instead of `.price`. The site appears to have been redesigned.

Let me verify:
> stagehand eval "document.querySelector('.product-price')?.textContent"

Yes, that returns "$29.99". I'll update the selector in your function:

[edits price-monitor.ts to use '.product-price']

Testing locally:
> stagehand fn invoke price-monitor --local -p '{"productUrl": "https://example.com/product/123"}'

Works! Deploying fix:
> stagehand fn publish price-monitor.ts

The function should work now. Would you like me to commit this fix?
```