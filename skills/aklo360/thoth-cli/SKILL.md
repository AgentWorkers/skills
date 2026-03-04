---
name: thoth-cli
version: 0.2.26
description: "Hermetic Divination CLI：  
- 占星术（出生星盘分析、星体运行预测、择日占卜、回归分析、星象配对）  
- 塔罗牌（基于加密随机数生成的卜卦结果）  
- 宝石学（希伯来语/希腊语/英语版本的数字解析）  
- 数字命理学（毕达哥拉斯学派的理论）  
**重要提示：**  
务必先运行该命令行工具（CLI）进行占卜操作；切勿自行伪造星体位置或塔罗牌结果。"
author: "aklo360"
homepage: "https://thothcli.com"
repository: "https://github.com/aklo360/thoth-cli"
license: "MIT"
metadata:
  openclaw:
    emoji: "𓅝"
    requires:
      bins: ["thoth"]
    install:
      - id: npm
        kind: node
        package: thoth-cli
        bins: ["thoth"]
        label: "Install thoth-cli from npm"
        registry: "https://www.npmjs.com/package/thoth-cli"
---
# thoth-cli — 隐秘占卜工具

𓅝 **v0.2.26** | 瑞士星历 • secrets.SystemRandom • 古典吉玛塔（Gematria） • 毕达哥拉斯数字命理学

**来源:** https://github.com/aklo360/thoth-cli  
**npm:** https://www.npmjs.com/package/thoth-cli  
**官方网站:** https://thothcli.com

## ⚖️ 重要规则

**切勿伪造行星位置、抽牌结果或计算出的数值。请先运行命令行工具（CLI），再进行解读。**

```
CLI = DATA (empirical)    →    Agent = INTERPRETATION (Hermetic)
```

---

## 安装

该软件包由 `aklo360` 在 npm 上发布。详情请访问：https://www.npmjs.com/package/thoth-cli

---

## 占星学

### 出生星盘  
```bash
thoth chart --date 1879-03-14 --time 11:30 --city "Ulm" --nation DE
```

### 行星运行（Transits）  
```bash
thoth transit --natal-date 1879-03-14 --natal-time 11:30 --city "Ulm" --nation DE
```

### 选择时刻（Optimal Timing）  
```bash
thoth electional --start 2026-03-15 --end 2026-04-15
thoth electional --start 2026-03-15 --end 2026-04-15 --city "NYC" --nation US --json
```  
*输出内容：VOC 月亮位置、逆行状态、行星相位、质量评分（优秀/良好/具有挑战性）*

### 其他占卜结果  
```bash
thoth solar-return --natal-date 1879-03-14 --natal-time 11:30 --city "Ulm" --nation DE --year 2026
thoth lunar-return --natal-date 1879-03-14 --natal-time 11:30 --city "Ulm" --nation DE --year 2026 --month 3
```

### 人际关系  
```bash
thoth synastry --date1 ... --date2 ...
thoth composite --date1 ... --date2 ...
thoth score --date1 ... --date2 ...
```

### 其他功能  
```bash
thoth horary --question "Should I?" --city "NYC"
thoth moon -e
thoth ephemeris --body pluto
thoth ephemeris-multi --bodies sun,moon,mercury --from 2026-03-01 --to 2026-03-31
thoth transit-scan --natal-date ... --start-year 2026 --end-year 2027
```

---

## 塔罗牌  
```bash
thoth tarot                   # Single card
thoth tarot -s 3-card         # Past/Present/Future
thoth tarot -s celtic         # Celtic Cross (10)
thoth tarot -q "Question?"    # With context
thoth tarot-card "The Tower"  # Card lookup
thoth tarot-spreads           # List spreads
```

---

## 吉玛塔（Gematria）  
```bash
thoth gematria "THOTH"
thoth gematria "Love" --compare "Will"
thoth gematria-lookup 93
```

---

## 数字命理学  
```bash
thoth numerology --date 1991-07-08 --name "Full Name"
thoth numerology-year --date 1991-07-08
```

---

## 完整文档

如需查看完整的命令行工具文档及所有命令，请访问：https://thothcli.com/skill.md