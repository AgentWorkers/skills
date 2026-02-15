---
name: smart-meme-generator
description: 这款由人工智能驱动的模因生成器能够根据任何主题或情境创建出完美且具有上下文意识的模因。无论用户是需要制作模因、寻找反应图片、将笑话可视化，还是需要适合在社交媒体上传播的内容，这款工具都能派上用场。它能够自动选择最合适的模因模板，并根据具体情况生成幽默的文字说明。
---

# 智能模因生成器 🎭  
能够根据任何主题生成真实的模因图片。使用免费的 imgflip API 来生成图片，并返回可分享的 URL。  

## 工作原理  
分为两个步骤：  
1. **模板选择**：分析主题关键词，选择最适合的模因格式。  
2. **图片生成**：通过 imgflip API 使用用户提供的文字说明来创建模因图片。  

用户负责提供创意性的文字说明，脚本负责匹配模板并生成图片。  

## 命令  
### 为某个主题选择最佳模板  
```bash
python3 scripts/generate_meme.py "your topic here"
```  
返回推荐的模板及所需框数。  

### 生成模因图片  
```bash
python3 scripts/generate_meme.py --template drake --captions "Bad option" "Good option"
```  
返回模因图片的 URL（例如：`https://i.imgflip.com/xxxxx.jpg`）。  

### 列出所有模板  
```bash
python3 scripts/generate_meme.py --list
```  

### JSON 输出（用于自动化）  
```bash
python3 scripts/generate_meme.py --template drake --captions "text1" "text2" --json
```  

## 可用模板（20 多种）  
| 关键字 | 名称 | 需要的框数 | 适用主题 |  
|-------|------|-------|---------|  
| drake | Drake Hotline Bling | 2 | 比较、偏好 |  
| distracted | Distracted Boyfriend | 3 | 诱惑、改变忠诚度 |  
| fine | This Is Fine | 2 | 混乱、否认、一切皆乱 |  
| brain | Expanding Brain | 4 | 等级提升、高智商表现 |  
| cat | Woman Yelling at Cat | 2 | 争吵、困惑 |  
| change | Change My Mind | 1 | 火热的观点、有争议的意见 |  
| buttons | Two Buttons | 3 | 难以做出的选择、困境 |  
| pikachu | Surprised Pikachu | 2 | 显而易见/可预测的结果 |  
| stonks | Stonks | 1 | 金钱、交易、加密货币 |  
| panik | Panik Kalm Panik | 3 | 从恐慌到平静的情景 |  
| buff_doge | Buff Doge vs Cheems | 4 | 过去与现在的对比 |  
| uno | UNO Draw 25 | 2 | 拒绝做某事 |  
| always_has_been | Always Has Been | 2 | 新发现 |  
| gru_plan | Gru’s Plan | 4 | 失败的计划 |  
| trade_offer | Trade Offer | 3 | 交易、交换 |  
| bernie | Bernie Asking | 1 | 重复的请求 |  
| left_exit | Left Exit Off Ramp | 3 | 忽视显而易见的选择 |  
| disaster_girl | Disaster Girl | 2 | 邪恶的满足感 |  
| hide_pain | Hide the Pain Harold | 2 | 假装一切正常 |  
| think_about_it | Think About It | 2 | 复杂的逻辑推理 |  

## 用户使用流程  
当用户请求生成模因时：  
1. 使用主题关键词选择合适的模板。  
2. 编写符合模板风格的幽默文字说明。  
3. 使用 `--captions` 参数生成图片。  
4. 将图片 URL 发送给用户。  

**文字说明提示：**  
- 文字要简短——模因不是长篇大论。  
- 使用网络幽默的常见表达方式（小写、不使用句号、具体而非泛泛而谈）。  
- 与模板风格相匹配（例如：drake 模板适合表达偏好，pikachu 模板适合描述显而易见的结果）。  
- 确保文字与主题紧密相关——泛泛的说明通常不会有趣。  

## 设置  
该工具附带一个免费的 imgflip 账户。如需使用自己的账户：  
```bash
export IMGFLIP_USER="your_username"
export IMGFLIP_PASS="your_password"
```  
请访问 https://imgflip.com/signup 进行免费注册。  

## 依赖项  
无——仅依赖 Python 标准库（urllib）。