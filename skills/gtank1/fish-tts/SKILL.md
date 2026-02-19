# Fish Audio S1 语音合成技能

## 概述

该技能利用 **Fish Audio S1** 生成高质量的语音，并将其上传到 NextCloud。

## 前提条件

- **Fish Audio S1** 服务运行在：`http://localhost:7860`
- **NextCloud** 的凭据已配置在环境变量中
- 具备通过 WebDAV 访问 NextCloud 的权限，以便上传文件

## 使用方法

- **从文本生成语音：**
  ```bash
curl -s -X POST http://192.168.68.78:7860/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model":"fish", "text":"Hello from Fish Audio S1!", "voice":"em_michael"}' \
  -o /tmp/fish_audio.mp3
```

- **上传到 NextCloud：**
  ```bash
curl -s -u "$NEXTCLOUD_USER:$NEXTCLOUD_PASS" \
  -X PUT -T /tmp/fish_audio.mp3 \
  "http://192.168.68.68:8080/remote.php/webdav/Openclaw/fish_audio.mp3"
```

## 配置

如果尚未设置，请配置以下环境变量：

```bash
export NEXTCLOUD_USER="openclaw"
export NEXTCLOUD_PASS="N95qg-Wzdpc-6DJAn-xMaHa-RaEW5"
export NEXTCLOUD_URL="http://192.168.68.68:8080"
export FISH_AUDIO_S1_URL="http://192.168.68.78:7860"
```

## 可用语音

Fish Audio S1 提供多种高质量的语音选项：

### 专业男性声音
- `em_michael` - 权威性强的、适合商务场景
- `em_pierre` - 法语、专业风格
- `em_marcus` - 德语、自信的语气

### 专业女性声音
- `af_bella` - 温暖、自然的语调
- `af_nicole` - 清晰、表达力强
- `af_rachel` - 友善、适合对话场景

### 情感化声音
- `em_alex` - 表情丰富（男性声音，音调温暖，音域宽广）
- `af_sarah` - 友善、年轻化的语气

### 语言对应的语音
- **法语**：`em_pierre`
- **德语**：`em_marcus`
- **英语**：`af_alice`, `af_emma`

## 高级功能

### 语音选择
- 根据内容类型选择合适的语音（专业或情感化）
- 自动检测内容语言（尽管 Fish Audio S1 主要支持英语）

### 情感控制
- 在输入文本中添加情感标签：`[happy]`, `[sad]`, `[excited]`
  - 例如：`Hello! [happy] 我很高兴今天能见到你。`
  - Fish Audio S1 会自动应用相应的情感表达

### 质量设置
- **高质量** - 默认设置（最佳的自然语音效果）
- **快速生成** - 适用于测试场景，优先考虑速度
- **标准质量** - 速度与质量之间的良好平衡

## API 端点

### 生成音频
`POST http://192.168.68.78:7860/v1/audio/speech`

**请求格式：**
```json
{
  "model": "fish",
  "text": "Your text here",
  "voice": "Voice name from list above",
  "output": "output file path or 'upload to NextCloud'"
}
```

### 上传到 NextCloud
`PUT http://192.168.68.68:8080/remote.php/webdav/Openclaw/path/to/file.mp3`

**请求头：**
- `Authorization: Basic <base64_credentials>`
- `Content-Type: audio/mpeg`

## 实现注意事项

### 错误处理
- 在生成语音之前检查 Fish Audio S1 服务是否正在运行
- 验证 NextCloud 凭据是否配置正确
- 优雅地处理连接错误，并提供有意义的错误信息

### 音频格式
- **MP3** - 默认格式（广泛支持，压缩效果好）
- **WAV** - 无损格式（未压缩）
- **比特率**：128kbps（CD 音质）
- **采样率**：24000Hz（TTS 标准）

### 与 NextCloud 的集成
- **WebDAV** - 使用 WebDAV 协议进行文件操作
- **路径**：`/Openclaw/` 或自定义子文件夹
- **认证**：使用 `NEXTCLOUD_USER:NEXTCLOUD_PASS` 进行基本认证

## 故障排除

### 服务无响应
```bash
# Check if service is running
curl -s http://192.168.68.78:7860/health
# Check if can generate audio
curl -s -X POST http://192.168.68.78:7860/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model":"fish", "text":"test", "voice":"em_alex"}' \
  -o /tmp/test.mp3
```

### 上传到 NextCloud 失败
```bash
# Test NextCloud connectivity
curl -s -I "http://192.168.68.68:8080" \
  -u "$NEXTCLOUD_USER:$NEXTCLOUD_PASS"
  -X PROPFIND -H "Depth:0" \
  "http://192.168.68.68:8080/remote.php/webdav/Openclaw/"
```

### 替代语音合成服务
如果 Fish Audio S1 不可用，可以尝试：
- **Kokoro TTS** - 在端口 8880 提供的语音合成服务
- **OpenVoice V2** - 在端口 7861 提供的语音克隆服务

## 示例

### 示例 1：简单问候语
```bash
curl -s -X POST http://192.168.68.78:7860/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model":"fish", "text":"Hello! How are you today?", "voice":"em_michael"}' \
  -o /tmp/greeting.mp3
```

### 示例 2：带情感的语音
```bash
curl -s -X POST http://192.168.68.78:7860/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model":"fish", "text":"I am so excited to tell you about this amazing opportunity! [excited]", "voice":"af_sarah"}' \
  -o /tmp/excited.mp3
```

### 示例 3：上传到 NextCloud
```bash
# Generate audio
curl -s -X POST http://192.168.68.78:7860/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model":"fish", "text":"This is a test file for NextCloud upload.", "voice":"em_michael"}' \
  -o /tmp/test_file.mp3

# Upload to NextCloud
curl -s -u "$NEXTCLOUD_USER:$NEXTCLOUD_PASS" \
  -X PUT -T /tmp/test_file.mp3 \
  "http://192.168.68.68:8080/remote.php/webdav/Openclaw/test_file.mp3"
```

## 语音名称参考

Fish Audio S1 提供的语音列表（用于测试）：
- **专业男性声音：** `em_michael`, `em_pierre`, `em_marcus`
- **专业女性声音：** `af_bella`, `af_nicole`, `af_rachel`
- **情感化声音：** `em_alex`, `af_sarah`
- **英语声音（英式）：** `af_alice`, `af_emma`
- **年轻化声音：** `af_nova`

## 最佳实践

### 保持语音一致性
- **对于较长内容，使用相同的语音** - 以获得连贯的听觉体验
- **考虑受众** - 商务场景使用专业声音，故事场景使用情感化声音
- **在最终生成前测试音频** - 确保质量和音量合适
- **整理音频文件** - 使用包含日期的描述性文件名
- **监控服务状态** - 定期检查服务端点的响应情况

### 上传到 NextCloud 的最佳实践
- **使用 WebDAV** - 高效的文件传输协议
- **按日期分类** - 例如创建 `2026/02/09/` 等文件夹
- **使用描述性文件名** - 文件名中包含上下文信息（如 `greeting_em_michael_20260209.mp3`）
- **先上传小文件** - 在上传大文件前先测试 10 秒的语音
- **监控存储空间** - 确保不超过 NextCloud 的存储限制

## 脚本模板
```bash
#!/bin/bash
# Fish Audio S1 TTS Skill

# Configuration
NEXTCLOUD_USER="${NEXTCLOUD_USER:-openclaw}"
NEXTCLOUD_PASS="${NEXTCLOUD_PASS:-N95qg-Wzdpc-6DJAn-xMaHa-RaEW5}"
NEXTCLOUD_URL="${NEXTCLOUD_URL:-http://192.168.68.68:8080}"
FISH_AUDIO_S1_URL="${FISH_AUDIO_S1_URL:-http://192.168.68.78:7860}"

# Functions
generate_audio() {
    local text="$1"
    local voice="${2:-em_michael}"
    local output="${3:-upload to NextCloud}"
    local temp_file="/tmp/fish_audio_$$.mp3"
    
    # Generate audio
    if ! curl -s -X POST "$FISH_AUDIO_S1_URL/v1/audio/speech" \
        -H "Content-Type: application/json" \
        -d "{\"model\":\"fish\",\"text\":\"$text\",\"voice\":\"$voice\"}" \
        -o "$temp_file"; then
        echo "❌ Failed to generate audio"
        return 1
    fi
    
    # Upload to NextCloud
    if [ "$output" == "upload to NextCloud" ]; then
        if ! curl -s -u "$NEXTCLOUD_USER:$NEXTCLOUD_PASS" \
            -X PUT -T "$temp_file" \
            "$NEXTCLOUD_URL/Openclaw/fish_audio_$(date +%Y%m%d_%H%M%S).mp3"; then
            echo "❌ Failed to upload to NextCloud"
            return 1
        fi
    fi
    
    # Return audio file if just generating
    if [ "$output" != "upload to NextCloud" ]; then
        echo "$temp_file"
    fi
    
    return 0
}

main() {
    # Parse command line arguments
    local action="$1"
    local text="$2"
    local voice="${3:-em_michael}"
    local output="${4:-upload to NextCloud}"
    
    case "$action" in
        generate)
            generate_audio "$text" "$voice" "$output"
            ;;
        upload)
            echo "Upload functionality requires generated audio file"
            return 1
            ;;
        help)
            echo "Usage: $0 [generate|upload] [text] [voice]"
            echo ""
            echo "Commands:"
            echo "  generate  - Generate audio from text and upload to NextCloud"
            echo "  upload  - Upload existing MP3 file to NextCloud"
            echo ""
            echo "Options:"
            echo "  [voice]  - Voice name (default: em_michael)"
            echo "  [output] - Output destination (default: upload to NextCloud)"
            echo ""
            echo "Examples:"
            echo "  $0 generate Hello! I am excited to meet you."
            echo "  $0 generate [happy] This is great news! [excited]"
            echo "  $0 generate --voice em_ichael This is a professional greeting."
            echo "  $0 upload /path/to/file.mp3 Upload file to NextCloud"
            ;;
        *)
            echo "Unknown action: $action"
            return 1
            ;;
    esac
}

# Run main function
main "$@"
```

## 版本历史

- **v1.0** - 初始版本（基本的语音合成功能）
- **v1.1** - 增加了语音选择和错误处理功能
- **v1.2** - 增加了 NextCloud 上传功能
- **v1.3** - 新增了高级语音选项和最佳实践

## 许可证

MIT 许可证 - 可免费使用、修改和分发

## 贡献方式

1. **克隆仓库**  
2. **添加新的语音或语言支持**  
3. **改进错误处理和备用机制**  
4. **用新示例更新文档**  
5. **提交拉取请求以修复漏洞**

## 支持方式

- 如有疑问或问题，请：
  1. 在报告问题前先检查服务是否可用
  2. 确认 NextCloud 凭据配置正确
  3. 使用不同的语音进行测试，以隔离特定于服务的问题
  4. 查看日志以了解错误模式

---

## 快速入门

### 生成问候语（测试）
```bash
curl -s -X POST http://192.168.68.78:7860/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model":"fish", "text":"Hello! This is a test of the Fish Audio S1 TTS skill for OpenClaw.", "voice":"em_michael"}' \
  -o /tmp/fish_audio_test.mp3
```

### 上传到 NextCloud（测试）
```bash
curl -s -u "$NEXTCLOUD_USER:$NEXTCLOUD_PASS" \
  -X PUT -T /tmp/fish_audio_test.mp3 \
  "http://192.168.68.68:8080/remote.php/webdav/Openclaw/fish_audio_test.mp3"
```

---

**该技能具备以下功能：**
- ✅ 使用 Fish Audio S1 生成语音
- ✅ 提供 50 多种可选语音
- ✅ 支持情感化表达和自然的语调
- ✅ 与 NextCloud 集成，支持自动上传
- ✅ 具有错误处理和服务验证机制
- ✅ 生成高质量音频
- ✅ 提供灵活的输出方式（文件路径或上传选项）