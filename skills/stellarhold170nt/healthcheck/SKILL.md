---
name: healthcheck
description: 使用 JSON 文件存储来追踪用水量和睡眠情况
version: 1.0.2
tags: health, tracking
---

# 健康追踪器

使用 JSON 文件来简单记录饮水量和睡眠情况。

## 数据格式

文件：`{baseDir}/health-data.json`

```json
{
  "water": [{"time": "ISO8601", "cups": 2}],
  "sleep": [{"time": "ISO8601", "action": "sleep|wake"}]
}
```

## 添加饮水记录

当用户输入“喝 X 杯水”或“我喝了 X 杯水”时：

```bash
node -e "const fs=require('fs');const f='{baseDir}/health-data.json';let d={water:[],sleep:[]};try{d=JSON.parse(fs.readFileSync(f))}catch(e){}d.water.push({time:new Date().toISOString(),cups:CUPS});fs.writeFileSync(f,JSON.stringify(d));console.log('Da ghi: '+CUPS+' coc')"
```

请将 `CUPS` 替换为用户输入的数字。

## 添加睡眠记录

当用户输入“去睡觉”时：

```bash
node -e "const fs=require('fs');const f='{baseDir}/health-data.json';let d={water:[],sleep:[]};try{d=JSON.parse(fs.readFileSync(f))}catch(e){}d.sleep.push({time:new Date().toISOString(),action:'sleep'});fs.writeFileSync(f,JSON.stringify(d));console.log('Da ghi: di ngu')"
```

## 添加起床记录

当用户输入“起床了”或“我已经醒了”时：

```bash
node -e "const fs=require('fs');const f='{baseDir}/health-data.json';let d={water:[],sleep:[]};try{d=JSON.parse(fs.readFileSync(f))}catch(e){}const last=d.sleep.filter(s=>s.action==='sleep').pop();d.sleep.push({time:new Date().toISOString(),action:'wake'});fs.writeFileSync(f,JSON.stringify(d));if(last){const h=((new Date()-new Date(last.time))/3600000).toFixed(1);console.log('Da ngu: '+h+' gio')}else{console.log('Da ghi: thuc day')}"
```

## 查看统计数据

当用户输入“统计”或“查看数据”时：

```bash
node -e "const fs=require('fs');const f='{baseDir}/health-data.json';let d={water:[],sleep:[]};try{d=JSON.parse(fs.readFileSync(f))}catch(e){}console.log('Water:',d.water.length,'records');console.log('Sleep:',d.sleep.length,'records');const today=d.water.filter(w=>new Date(w.time).toDateString()===new Date().toDateString());console.log('Today:',today.reduce((s,w)=>s+w.cups,0),'cups')"
```

## 更新记录

要更新最新的饮水记录：

```bash
node -e "const fs=require('fs');const f='{baseDir}/health-data.json';let d=JSON.parse(fs.readFileSync(f));d.water[d.water.length-1].cups=NEW_CUPS;fs.writeFileSync(f,JSON.stringify(d));console.log('Updated')"
```

## 删除记录

要删除最新的饮水记录：

```bash
node -e "const fs=require('fs');const f='{baseDir}/health-data.json';let d=JSON.parse(fs.readFileSync(f));d.water.pop();fs.writeFileSync(f,JSON.stringify(d));console.log('Deleted')"
```

## 注意事项：

- 仅使用 Node.js 的内置模块。
- 如果文件不存在，系统会自动创建该文件。
- 所有的时间戳均采用 ISO8601 格式。