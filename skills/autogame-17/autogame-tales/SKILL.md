# AutoGame Tales (autogame-tales)

这是一项用于记录和描述 AutoGame 中出现的“超自然”错误（bug）和故障的技能，它能够将这些奇怪的日志转化为“鬼故事”（即生动、引人入胜的叙述形式）。

## 工具

### `node skills/autogame-tales/index.js`
该脚本负责生成并发送一张“鬼故事”卡片到 Feishu 平台。

**参数：**
- `--title <string>`：异常现象的标题（例如：“时间倒流”）。
- `--victim <string>`：遇到该问题的用户。
- `--desc <string>`：错误现象的详细描述。
- `--target <id>`：目标 Feishu 聊天 ID 或用户 ID。

## 使用方法
```bash
node skills/autogame-tales/index.js --title "The Endless Death Loop" --victim "Li Mingxuan" --desc "Hearing 'I died' repeatedly while logs counted backwards." --target "oc_xxx"
```