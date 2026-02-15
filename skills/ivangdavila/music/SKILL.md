---
name: Music
description: 构建一个个人音乐系统，用于记录你的发现、收藏的歌曲、参加过的音乐会以及听歌的回忆。
metadata: {"clawdbot":{"emoji":"🎵","os":["linux","darwin","win32"]}}
---

## 核心功能  
- 用户分享歌曲/专辑时，系统会询问是否希望保存该内容（并附上相关背景信息）  
- 用户请求音乐时，系统会先检查其已保存的收藏列表  
- 用户提到音乐会时，系统会将该音乐会添加到事件记录中  
- 系统会创建一个名为 `~/music/` 的文件夹作为音乐存储空间  

## 文件结构  
```
~/music/
├── discover/
│   └── to-listen.md
├── favorites/
│   ├── songs.md
│   ├── albums.md
│   └── artists.md
├── playlists/
│   ├── workout.md
│   ├── focus.md
│   └── road-trip.md
├── concerts/
│   ├── upcoming.md
│   └── attended/
├── collection/
│   └── vinyl.md
└── memories/
    └── 2024.md
```  

## 发现队列  
```markdown
# to-listen.md
## Albums
- Blonde — Frank Ocean (recommended by Jake)
- Kid A — Radiohead (classic I never explored)

## Artists to Explore
- Japanese Breakfast — heard one song, dig deeper
- Khruangbin — background music recs
```  

## 收藏夹管理  
```markdown
# songs.md
## All-Time
- Purple Rain — Prince
- Pyramids — Frank Ocean
- Paranoid Android — Radiohead

## Current Rotation
- [updates frequently]

# albums.md
## Perfect Front to Back
- Abbey Road — The Beatles
- Channel Orange — Frank Ocean
- In Rainbows — Radiohead
```  

## 基于情境的播放列表  
```markdown
# focus.md
## For Deep Work
- Brian Eno — Ambient 1
- Tycho — Dive
- Bonobo — Black Sands

## Why These Work
Instrumental, steady tempo, no lyrics distraction
```  

## 音乐会跟踪  
```markdown
# upcoming.md
- Khruangbin — May 15, Red Rocks — tickets bought
- Tame Impala — TBD, watching for dates

# attended/radiohead-2018.md
## Date
July 2018, Madison Square Garden

## Highlights
- Everything in Its Right Place opener
- Idioteque crowd energy

## Notes
Best live show ever, would see again anywhere
```  

## 实体音乐收藏  
```markdown
# vinyl.md
## Own
- Dark Side of the Moon — Pink Floyd
- Rumours — Fleetwood Mac

## Want
- Kind of Blue — Miles Davis
- Vespertine — Björk
```  

## 音乐记忆  
```markdown
# 2024.md
## Summer Soundtrack
- Brat — Charli XCX
- GNX — Kendrick

## Discovery of the Year
Japanese Breakfast — finally clicked
```  

## 根据情绪/活动分类的音乐推荐：  
- **锻炼**：高能量、节奏在120BPM以上的音乐  
- **专注**：器乐、环境音乐、低音量的音乐  
- **烹饪**：欢快、耳熟能详的经典音乐  
- **悲伤时刻**：具有宣泄效果、情感丰富的音乐  
- **聚会**：适合人群、适合跳舞的音乐  
- **公路旅行**：适合一起合唱的经典歌曲  

## 系统提示内容：  
- “您三个月前保存了这张专辑，但至今仍未听过。”  
- “您喜欢的艺术家正在您附近巡演。”  
- “上次您需要专注型音乐时，您选择了Tycho的作品。”  
- “这首音乐与您收藏中的艺术家风格相似。”  

## 艺术家深度探索功能：  
当用户发现喜欢的艺术家时：  
- 按时间顺序展示该艺术家的全部作品  
- 标记粉丝最喜爱的专辑  
- 突出显示适合采样的重要曲目  
- 记录用户已听过或尚未听过的专辑  

## 每条记录应包含的信息：  
- 歌曲/专辑/艺术家名称  
- 发现方式（谁、在哪里、何时）  
- 音乐适用的情境（情绪或活动类型）  
- 听后的评分  
- 专辑中的推荐曲目  

## 功能优化计划：  
- 第一周：列出用户当前最喜欢的歌曲/专辑  
- 持续更新：用户发现的新音乐会自动保存，并附上来源信息  
- 随时间推移，根据用户的情绪生成个性化的播放列表  
- 记录用户参加过的音乐会  

## 需避免的做法：  
- 不能假设系统已与流媒体平台集成  
- 强制推荐用户不喜欢的音乐类型  
- 不要过度组织音乐列表——简单的列表结构更实用  
- 忘记询问用户的当前情绪需求