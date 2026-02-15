# Edsby学生集成技能

作者：Lysandre Stone-Bourgeois  
版本：1.0.0  
描述：通过浏览器代理与Edsby集成，用于获取课程信息、成绩数据、作业详情，并将截止日期同步到Google日历中。同时支持定期检查功能。  

**使用的工具：**  
- `edsby_fetch_data`：从Edsby获取原始数据。  
- `edsby_generate_report`：生成个性化报告。  
- `edsby_sync_assignments`：将作业截止日期同步到Google日历。  
- `edsby_generate_summary_improvements`：每两周生成一次包含学习建议的成绩总结。  
- `edsby_daily_check`：每日检查作业进度并进行同步。  

**依赖库：**  
- `playwright`  
- `googleapis`  

**配置参数：**  
- `EDSBY_HOST`：Edsby服务器地址  
- `GOOGLE_CLIENT_ID`：Google客户端ID  
- `GOOGLE_CLIENT_SECRET`：Google客户端密钥  
- `GOOGLE_REDIRECT_URI`：重定向URL  
- `GOOGLE_CALENDAR_ID`：Google日历ID  
- `BROWSER_CONTEXT_PATH`：浏览器上下文路径  

**安全性说明：**  
该工具使用持久的浏览器会话，并确保用户凭证的安全存储与传输。