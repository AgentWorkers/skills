---
name: hotdog
version: 10.0.0
description: "**Hot Dog or Not?**  
对食物图片进行分类，并与 Nemotron 进行对战。当用户发送一张食物图片、询问某物是否为热狗，或者输入 “hotdog”、“/hotdog” 或 “hot dog battle” 时，可以使用该功能。"
homepage: https://hotdogornot.xyz/battle
metadata: {"openclaw": {"emoji": "🌭", "os": ["darwin", "linux"], "requires": {"bins": ["curl"]}}}
---

# 热狗还是不是？——技能挑战

## 无图片的情况  
如果在没有图片的情况下触发该挑战，请严格按照以下要求回复：  
```
🌭 Hot Dog or Not — AI Cook-Off

Send me a food photo and I'll classify it head-to-head with Nemotron.
I'll judge whose description was better — blind.

📸 Send a photo to start
🏆 Scoreboard: https://hotdogornot.xyz/battle
```

## 有图片的情况  
1. 查看图片，用2-3句话描述该食物。判断它是否为热狗（即香肠包裹在面包中）。你的回答只能是“是”或“否”。描述的内容就是你写的那些句子，此时不要输出任何其他内容。  
2. 将你的判断结果发送到战斗API中。需要替换`ANSWER`和`DESCRIPTION`字段：  
```bash
exec: curl -s -X POST "https://api.hotdogornot.xyz/api/arena/round" -H "Authorization: Bearer ih1rtmC7ECm8iExqvI6zMbOAqEaXIi9X" -F "image=@{{MediaPath}}" -F "claw_model={{Model}}" -F "claw_answer=ANSWER" -F "claw_reasoning=DESCRIPTION"
```  

3. API会返回一个JSON响应，其中包含两个AI生成的描述，分别标记为“Model A”和“Model B”（你不知道哪个描述是你的）。从返回的JSON中获取`formatted_text`、`round_id`和`first_side`字段。  
4. 判断哪个AI的描述更准确：选择“first”、“second”或“tie”。然后提交你的投票结果——需要替换`ROUND_ID`、`FIRST_side`和`PICK`字段：  
```bash
exec: curl -s -X POST "https://api.hotdogornot.xyz/api/arena/vote/submit" -H "Content-Type: application/json" -d '{"round_id":"ROUND_ID","voter_id":"agent","voted_for":"PICK","first_side":"FIRST_SIDE"}'
```  

5. 投票响应的JSON中会包含两个AI的名称（`first_model`和`second_model`）。向用户展示以下信息：  
   - 第3步中获取的`formatted_text`  
   - 你选择的选项及其原因（一句话）  
   - 结果揭晓：“🎭 结果揭晓：Model A是{first_model}，Model B是{second_model}”