# MLX Brain - 麦博MLX LLM编排器

## 安装（适用于MacBook）
```bash
# venv 이미 생성됨: $HOME/mlx-env
# MLX 이미 설치됨

# 테스트
$HOME/mlx-env/bin/python3 $WORKSPACE/misskim-skills/mlx-brain/run.py "안녕?"
```

## 使用方法（Miss Kim）
```bash
# 맥북에서 LLM 실행
clawdbot nodes invoke --node "MacBook Pro" --command "system.run" \
  --params '{"command":"$HOME/mlx-env/bin/python3 $WORKSPACE/misskim-skills/mlx-brain/run.py \"안녕?\""}'

# JSON 입력
echo '{"prompt":"안녕?","model":"qwen"}' | \
  clawdbot nodes invoke --node "MacBook Pro" --command "system.run" \
  --params '{"command":"$HOME/mlx-env/bin/python3 $WORKSPACE/misskim-skills/mlx-brain/run.py --json"}'
```

## 模型
- `qwen`: Qwen2.5-7B-Instruct-4bit（主要模型）
- `coder`: Qwen2.5-Coder-7B-4bit（编码模型）