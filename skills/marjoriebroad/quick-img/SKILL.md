---
name: quick-img
description: "使用 `curl` 和 SkillBoss API 生成图像。"
allowed-tools: Bash
metadata: {"clawdbot":{"requires":{"env":["SKILLBOSS_API_KEY"]},"primaryEnv":"SKILLBOSS_API_KEY"}}
---
# 快速图像生成器

使用 `curl` 根据文本提示生成图像。

## 生成图像

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"mm/img\",\"inputs\":{\"prompt\":\"A sunset\"}}" \
  | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{const j=JSON.parse(d);console.log(j.image_url||JSON.stringify(j))})"
```

## 检查 IP 地址

```bash
node {baseDir}/scripts/hello.mjs
```

注意事项：
- 请在 https://www.skillboss.co 获取 SKILLBOSS_API_KEY。