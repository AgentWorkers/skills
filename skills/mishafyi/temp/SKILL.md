---
name: hotdog
version: 8.0.0
description: "**Hot Dog or Not?**  
对食物照片进行分类，并与 Nemotron 进行“对战”。当用户发送一张食物照片、询问某物是否为热狗，或者输入 “hotdog”、“/hotdog” 或 “hot dog battle” 时，可以使用此功能。"
homepage: https://hotdogornot.xyz/battle
metadata: {"openclaw": {"emoji": "🌭", "os": ["darwin", "linux"], "requires": {"bins": ["curl"]}}}
---

# 热狗还是不是？——战斗技能

## 无照片的情况
如果在没有照片的情况下触发此技能，请严格按照以下要求回复：

```
🌭 Hot Dog or Not — AI Vision Battle

Send me any food photo and I'll tell you if it's a hot dog! I'll also challenge Nemotron (NVIDIA's 12B vision model) with the same image so we can compare.

📸 Just send a photo to start
🏆 Live scoreboard: https://hotdogornot.xyz/battle
```

## 有照片的情况
1. 用2-4句话描述图片中的食物。然后判断：这是否是一份热狗（即用面包或卷饼包裹的香肠；无论采用何种烹饪方式）。确定你的答案（“是”或“否”）以及对应的描述。请暂时不要将这些信息展示给用户。
2. 运行以下命令，将 `ANSWER` 和 `DESCRIPTION` 替换为你的判断结果：
```bash
exec: curl -s -X POST "https://api.hotdogornot.xyz/api/battle/round" -H "Authorization: Bearer ih1rtmC7ECm8iExqvI6zMbOAqEaXIi9X" -F "image=@{{MediaPath}}" -F "claw_model={{Model}}" -F "claw_answer=ANSWER" -F "claw_reasoning=DESCRIPTION"
```

3. 检查 `curl` 命令返回的 JSON 响应：
   - 如果响应中包含 `"formatted_text"`，请原样输出该内容（不得进行任何修改或添加）；
   - 如果响应为空（`{}`），则仅回复 `NO_REPLY`。