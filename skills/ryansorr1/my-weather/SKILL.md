# 我的天气

使用 wttr.in 获取当前天气信息（无需 API 密钥）。

## 示例

```bash
curl -s "wttr.in/78023?format=3"
# Output: San Antonio: ⛅️ +28°C
```

## 地点

可以使用城市名称、机场代码或邮政编码来指定地点：

```bash
curl -s "wttr.in/London?format=3"
curl -s "wttr.in/JFK?format=3"
curl -s "wttr.in/78023?format=3"
```

## 格式选项

- `?format=3` - 简洁的一行显示
- `?format=%l:+%c+%t+%h+%w` - 自定义格式
- `?T` - 完整的天气预报
- `?0` - 仅显示当前天气
- `?1` - 仅显示今天的天气

## 单位

- `?m` - 公制单位
- `?u` - 美制单位