# feishu-calendar

用于管理 Feishu（Lark）日历。通过此技能可以列出日历、查看日程安排以及同步事件。

## 使用方法

### 列出日历
查看可用的日历及其 ID。
```bash
node skills/feishu-calendar/list_test.js
```

### 搜索日历
根据名称或摘要查找日历。
```bash
node skills/feishu-calendar/search_cal.js
```

### 查看主管的日历
专门查看主管的日历状态。
```bash
node skills/feishu-calendar/check_master.js
```

### 同步日历
运行日历同步流程（将事件同步到本地设备或内存中）。
```bash
node skills/feishu-calendar/sync_routine.js
```

## 设置要求
需要 `.env` 文件中的 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`。

## 标准协议：任务标记
**触发条件**：用户输入“标记此任务”或“提醒我...”。
**操作步骤**：
1. **解析指令**：提取日期/时间（例如：“2月4日” -> YYYY-MM-04）。
2. **执行操作**：运行 `create.js` 并将 `--attendees` 参数设置为请求者的 ID。
3. **格式化结果**：
   ```bash
   node skills/feishu-calendar/create.js --summary "Task: <Title>" --desc "<Context>" --start "<ISO>" --end "<ISO+1h>" --attendees "<User_ID>"
   ```

### 设置共享日历
为项目创建共享日历并添加成员。
```bash
node skills/feishu-calendar/setup_shared.js --name "Project Name" --desc "Description" --members "ou_1,ou_2" --role "writer"
```