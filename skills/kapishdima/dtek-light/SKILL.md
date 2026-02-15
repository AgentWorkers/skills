---
name: dtek-light-check
description: 通过敖德萨电力公司（ДТЭК Одесские электросети）的官方网站查询电力供应情况  
地址：敖德萨市叶夫根·奇卡伦卡街（Вул. Чикаленка Евгена），43号
---

# 检查电力供应情况（Odessa Electric Networks的DTEK服务）

该技能用于通过dtek-oem.com.ua网站查询Odessa市Chikalenka Yevgena街43号地址当前的电力供应情况。

## 使用场景

当用户询问以下问题时，请使用此技能：
- “电力供应情况如何？”
- “有电吗？”
- “什么时候能恢复供电？”
- “/light”

## 先决条件

需要安装了Chromium的Playwright框架：

```bash
npm install playwright
npx playwright install chromium
```

## 操作步骤

1. 运行检查脚本。该脚本位于此SKILL.md文件的同一目录下：

```bash
node "$(dirname "$(find ~/.claude/skills -name 'check-light.js' -path '*dtek-light*' | head -1)")/check-light.js"
```

2. 脚本会返回一个包含`status`字段的JSON对象。请根据返回的结果进行相应的处理：

### 如果`status` = `no_light`：

回复：

```
Света нет. Выключили в [start_time].
Скорее всего эти бляди включат в [restore_time].
```

其中`[start_time]`和`[restore_time]`为JSON中的字段值。

### 如果`status` = `light_on`：

回复：

```
Свет вроде как есть, но кто этих пиздюков знает.
```

### 如果`status` = `error`或`unknown`：

回复：

```
Не удалось проверить, сайт ДТЭК опять чудит. Попробуй позже.
```

如果存在错误，请显示相应的错误信息。