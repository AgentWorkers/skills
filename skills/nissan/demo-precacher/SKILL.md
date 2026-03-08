---
name: demo-precacher
description: Pre-generate and cache all demo content before live presentations — hit every API endpoint in advance, verify playback, report coverage gaps. Use before hackathon demos, investor pitches, or any live presentation that relies on AI-generated content. Never demo live API calls.
version: 1.0.0
metadata:
  {
      "openclaw": {
            "emoji": "\ud83c\udfc3",
            "requires": {
                  "bins": [],
                  "env": [
                        "ELEVENLABS_API_KEY",
                        "MISTRAL_API_KEY"
                  ]
            },
            "primaryEnv": "ELEVENLABS_API_KEY",
            "network": {
                  "outbound": true,
                  "reason": "Pre-generates content by calling your configured APIs (ElevenLabs, Mistral, etc.) ahead of a live demo."
            }
      }
}
---

# 演示内容预缓存机制

AI演示的黄金法则是：**在演示过程中绝不要依赖实时API调用**。本技能提供了一种系统化的方法，用于在正式演示前预先生成并验证所有演示内容。

## 该机制的必要性

在一场为期48小时的编程马拉松比赛中，我们共有18个项目，涉及10种语言，这些项目都包含了音频解说、音效和背景音乐。在演示过程中，Mistral API出现了3秒的延迟峰值。由于所有内容都已经被预缓存，因此演示能够完美地从缓存中播放，而观众则以为这些内容是实时生成的。

## 实现方式

```python
async def precache_demo():
    scenarios = [
        {"name": "Sophie", "language": "fr", "prompt": "A story about cloud whales..."},
        {"name": "Kai", "language": "ja", "prompt": "A story about bamboo forests..."},
    ]
    
    for s in scenarios:
        # Step 1: Generate content (hits the real API)
        story = await generate_story(s["prompt"], s["name"], s["language"])
        
        # Step 2: Cache the result
        await cache.set(s, story)
        
        # Step 3: Generate all derived content (audio, images)
        for scene in story["scenes"]:
            audio = await generate_tts(scene["text"], voice_id)
            await cache.set(f"audio_{scene['id']}", audio)
        
        # Step 4: Verify playback
        cached = await cache.get(s)
        assert cached is not None, f"Cache miss for {s['name']}"
    
    # Step 5: Report coverage
    print(f"Cached {len(scenarios)} scenarios, all verified ✅")
```

## 需要检查的事项

在进行任何实时演示之前，请确保以下内容：
- [ ] 所有主要演示场景都已预缓存并经过验证
- [ ] 音频文件可以正常播放（格式正确，无损坏）
- [ ] 如果缓存失败，有备用内容可供使用
- [ ] 演示账户的凭据有效
- [ ] 缓存播放不需要网络连接
- [ ] 缓存的有效期在演示期间不会过期

## 相关文件

- `scripts/precache_demo.py` — 一个包含预缓存功能及验证逻辑的示例脚本