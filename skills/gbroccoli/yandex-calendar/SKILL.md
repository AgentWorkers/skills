# 雅虎日历

通过 CalDAV（vdirsyncer + khal）管理雅虎日历

## 可用的命令

### 显示事件
- `vdirsyncer sync && khal list today` - 显示今天的事件
- `khal list today 7d` - 显示本周的事件
- `khal calendar` - 显示本月的日历

### 添加事件
```bash
khal new "ДАТА ВРЕМЯ" "ДЛИТЕЛЬНОСТЬ" "НАЗВАНИЕ" && vdirsyncer sync
```

示例：
- `khal new "2026-02-10 15:00" "1h" "与客户会面"`
- `khal new "明天 14:00" "30m" "打电话"`

### 搜索
```bash
khal search "текст для поиска"
```

## 机器人使用说明

当用户询问日历相关内容时，使用以下命令：

**“显示今天的事件”** 或 **“我今天有什么安排？”**
→ 执行：`vdirsyncer sync && khal list today`
→ 向用户显示结果

**“我这周有什么安排？”** 或 **“本周的事件有哪些？”**
→ 执行：`khal list today 7d`

**“在 [时间] 添加一个名为 [事件名称] 的会议”**
→ 执行：`khal new "日期 时间" "持续时间" "事件名称" && vdirsyncer sync`
→ 日期示例：`明天 15:00`、`2026-02-10 14:00`

**“查找与 [主题] 相关的事件”**
→ 执行：`khal search "主题"`

## 注意事项

- 在显示事件之前，请务必先同步日历数据：`vdirsyncer sync`
- 添加事件后也需要同步数据：`&& vdirsyncer sync`
- 如果 `vdirsyncer` 报错，请仅使用 `khal` 命令（不进行同步）
- 事件持续时间支持：30m（30分钟）、1h（1小时）、2h（2小时）