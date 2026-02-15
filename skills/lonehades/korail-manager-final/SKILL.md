---
名称：korail-manager  
版本：0.1.0  
描述：“Korail（KTX/SRT）预订自动化工具。支持查询、预订和实时监控票务信息。”  

工具：  
- 名称：korail_search  
  描述：在两个车站之间搜索列车信息。  
  参数：  
    类型：对象  
    属性：  
      dep：{ 类型：字符串，描述：“出发站（例如：首尔、大田）”  
      arr：{ 类型：字符串，描述：“到达站（例如：釜山、东大邱）”  
      date：{ 类型：字符串，描述：“日期格式（YYYYMMDD）（默认：今天）”  
      time：{ 类型：字符串，描述：“时间格式（HHMMSS）（默认：当前时间）”  
    必需参数：[dep, arr]  
  命令：["python3", "scripts/search.py"]  

- 名称：korail_watch  
  描述：实时监控可用座位情况并自动预订。预订成功后通过Telegram发送通知。  
  参数：  
    类型：对象  
    属性：  
      dep：{ 类型：字符串，描述：“出发站”  
      arr：{ 类型：字符串，描述：“到达站”  
      date：{ 类型：字符串，描述：“日期格式（YYYYMMDD）”  
      start_time：{ 类型：数字，描述：“开始时间（0-23）”  
      end_time：{ 类型：数字，描述：“结束时间（0-23）”  
      interval：{ 类型：数字，描述：“检查间隔（秒，默认：300）”  
    必需参数：[dep, arr, date]  
  命令：["python3", "scripts/watch.py"]  

- 名称：korail_cancel  
  描述：取消预订。  
  参数：  
    类型：对象  
    属性：  
      train_no：{ 类型：字符串，描述：“可选：要取消的具体列车编号。如果省略，则取消所有预订。”  
  命令：["python3", "scripts/cancel.py"]  

依赖库：  
  python  
    - requests  
    - pycryptodome