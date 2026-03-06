# Telegram营销审计命令处理技能

## 目的
处理Telegram的`/marketing_audit`命令，通过给定的输入触发营销编排（Marketing Orchestrator）技能，并返回最终报告。

## Telegram命令
- 命令：`/marketing_audit`
- 参数：`instagramHandle`（可选），`websiteDomain`（可选）

## 实现
```javascript
module.exports = async function marketingAuditHandler(context) {
  const { instagramHandle, websiteDomain } = context.args;

  if (!instagramHandle && !websiteDomain) {
    await context.reply("Please provide an Instagram handle or website domain (or both).");
    return;
  }

  await context.reply("Starting marketing audit. This may take a few minutes...");

  try {
    const result = await context.callSkill("marketing-orchestrator", {
      instagramHandle,
      websiteDomain,
    });

    if (result && result.reportMarkdown) {
      await context.reply(result.reportMarkdown);
    } else {
      await context.reply("Audit completed but no report was generated.");
    }
  } catch (err) {
    await context.reply("Error during marketing audit: " + err.message);
  }
};
```

## 注意事项
- 将此技能文件夹添加到OpenClaw的技能目录中。
- 通过OpenClaw配置或ClawHub注册一个使用此技能作为处理程序的Telegram命令`/marketing_audit`。
- 确保收集器（API密钥）的环境变量已设置。