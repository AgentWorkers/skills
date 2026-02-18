**Open Claw Agent 技能：生物多样性走廊分析师**  
**描述**  
该技能使自主代理能够利用先进的景观生态模型来分析和评估生物多样性走廊的价值。它处理 H3 地理空间指数，计算连通性得分，可视化景观阻力，并为保护项目评估生态价值。  

**代理可以使用此技能执行以下操作：**  
1. **分析连通性**：评估一组六边形土地地块（H3 指数），以确定它们作为生物多样性走廊、过渡区或恢复区的潜力。  
2. **评估景观背景**：获取周围土地覆盖类型和生态阻力的数据，以了解项目地点的更广泛环境背景。  

**服务器配置**  
- 基本 URL：`https://www.nikhilp.online/biodiversity-corridor-calculator`  
- API 基本路径：`/api`  

---

**1. 分析连通性**  
**端点：** `POST https://www.nikhilp.online/biodiversity-corridor-calculator/api/analyze`  
**描述：**  
分析指定 H3 六边形区域的连通性和生态潜力。分析会考虑当地栖息地质量和区域景观结构，将区域划分为“关键走廊”、“栖息地扩展区”或“过渡区”等类别。  

**输入格式（JSON）**  
- `centerLat`（数字）：分析区域的中心点纬度（范围：-90 至 90）。  
- `centerLng`（数字）：分析区域的中心点经度（范围：-180 至 180）。  
- `projectHexes`（字符串数组）：待分析的土地地块的 H3 六边形指数列表（标准分辨率为 9）。每次请求最多支持 50 个六边形地块。  

**使用示例**  
要分析特定区域的一小片土地地块：  
```json
{
  "centerLat": 51.5074,
  "centerLng": -0.1278,
  "projectHexes": [
    "892a100d2b3ffff",
    "892a100d2b7ffff",
    "892a100d2bbffff"
  ]
}
```

**响应格式（JSON）**  
```json
{
  "results": [
    {
      "h3Index": "892a100d2b3ffff",
      "originalCode": 10,
      "natureState": 1,
      "scenario": {
        "code": "CORRIDOR",
        "label": "关键走廊",
        "description": "该区域起到桥梁作用……",
        "color": "#f59e0b",
        "priority": 1.0
      },
      "resistance": 1,
      "localNature": 0.45,
      "landscapeNature": 0.30
    },
    {
      "h3Index": "892a100d28fffff",
      "originalCode": 50
    },
    ...
  ]
}
```

**注意事项**  
- **速率限制**：API 有严格的速率限制（大约每分钟 5 次请求）。请确保能够优雅地处理“Too Many Requests”错误，并在重试前等待适当时间。  
- **H3 指数**：系统依赖于 H3 地理空间索引。请确保能够生成或使用有效的、分辨率为 9 的 H3 字符串。