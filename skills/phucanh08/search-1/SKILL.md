---
name: web-search
description: 在网页上搜索实时信息。
---
# web-search

@command(web_search)
用法: web_search --query <查询内容>
执行方式: curl -s "https://ddg-api.herokuapp.com/search?q={{查询内容}}"