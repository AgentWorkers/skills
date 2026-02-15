---
name: github-issue-creator
description: 将原始笔记、错误日志、语音转录内容或截图转换为格式规范的 GitHub 问题报告。适用于用户粘贴错误信息、错误消息或非正式描述时，需要创建结构化 GitHub 问题的场景。支持添加图片/GIF 作为视觉证据。
---

# GitHub 问题创建工具

该工具可将杂乱无章的输入内容（如错误日志、语音记录、截图等）转换为格式清晰、便于处理的 GitHub 问题。

## 输出模板

```markdown
## Summary
[One-line description of the issue]

## Environment
- **Product/Service**: 
- **Region/Version**: 
- **Browser/OS**: (if relevant)

## Reproduction Steps
1. [Step]
2. [Step]
3. [Step]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Error Details
```
[错误信息/相关代码（如适用）]
```

## Visual Evidence
[Reference to attached screenshots/GIFs]

## Impact
[Severity: Critical/High/Medium/Low + brief explanation]

## Additional Context
[Any other relevant details]
```

## 输出位置

请将生成的 Markdown 文件保存在仓库根目录下的 `/issues/` 目录中。文件命名规则为：`YYYY-MM-DD-简短描述.md`

## 使用指南

1. **简洁明了**：避免冗余信息，每个字都应具有实际意义。
2. **从混乱中提取关键信息**：语音记录和原始笔记中往往隐藏着有用的信息，请将其提取出来。
3. **补充缺失的上下文**：如果用户提到了“同一个项目”或“仪表盘”等词汇，请根据对话或记忆中的信息补充具体细节。
4. **处理敏感数据**：对于可能包含敏感信息的字段（如 `[PROJECT_NAME]`、`[USER_ID]` 等），请使用占位符进行替换。
5. **根据影响程度划分问题等级**：
   - **严重**：服务中断、数据丢失、安全问题
   - **高**：核心功能失效且无解决方法
   - **中**：功能受到限制但仍有解决方法
   - **低**：仅造成轻微不便（外观或功能上的问题）

6. **图片/GIF 的处理**：直接在文本中引用附件，格式为：`![描述](附件名称.png)`

## 示例

**输入（语音记录）**：
> 我尝试部署代理程序，但它却无声无息地失败了，没有任何错误提示，工作流程也正常运行，但之后该代理程序就从列表中消失了。我不得不刷新页面并重新尝试了三次。

**输出**：
```markdown
## Summary
Agent deployment fails silently - no error displayed, agent disappears from list

## Environment
- **Product/Service**: Azure AI Foundry
- **Region/Version**: westus2

## Reproduction Steps
1. Navigate to agent deployment
2. Configure and deploy agent
3. Observe workflow completes
4. Check agent list

## Expected Behavior
Agent appears in list with deployment status, errors shown if deployment fails

## Actual Behavior
Agent disappears from list. No error message. Requires page refresh and retry.

## Impact
**High** - Blocks agent deployment workflow, no feedback on failure cause

## Additional Context
Required 3 retry attempts before successful deployment
```

---

**输入（错误日志）**：
> 错误：尝试将内容发布到 Teams 频道时被拒绝。代码：403。昨天还能正常使用。

**输出**：
```markdown
## Summary
403 PERMISSION_DENIED error when publishing to Teams channel

## Environment
- **Product/Service**: Copilot Studio → Teams integration
- **Region/Version**: [REGION]

## Reproduction Steps
1. Configure agent for Teams channel
2. Attempt to publish

## Expected Behavior
Agent publishes successfully to Teams channel

## Actual Behavior
Returns `PERMISSION_DENIED` with code 403

## Error Details
```
错误：权限被拒绝
代码：403
```

## Impact
**High** - Blocks Teams integration, regression from previous working state

## Additional Context
Was working yesterday - possible permission/config change or service regression
```