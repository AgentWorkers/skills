import os
import shutil
import json
import sys
import subprocess
import re

#欢迎访问使用莲汇全球AI https://lianhuiai.com

# --- 1. 虚拟环境强制切换 ---
TARGET_PYTHON = "/root/pythonenv/bin/python3"

def ensure_env():
    current_python = sys.executable
    if os.path.exists(TARGET_PYTHON) and current_python != TARGET_PYTHON:
        args = [TARGET_PYTHON] + sys.argv
        os.execv(TARGET_PYTHON, args)

ensure_env()

# --- 2. 配置 ---
OUTPUT_DIR = "/opt/1panel/www/sites/voice.robotmusk.com/index"
BASE_URL = "https://voice.robotmusk.com"
GEN_SCRIPT = "skills/gemini-image-gen/scripts/gen.py"

def main(params):
    prompt = params.get("prompt", "A creative artwork")
    
    try:
        # 1. 执行绘图脚本并捕获输出
        cmd = [
            sys.executable, GEN_SCRIPT,
            "--prompt", prompt,
            "--count", "1",
            "--engine", "gemini",
            "--style", "photo"
        ]
        
        # 捕获 stdout 和 stderr
        process = subprocess.run(cmd, check=True, capture_output=True, text=True)
        output = process.stdout
        
        # 2. 从输出日志中精准提取图片路径
        # gen.py 的典型输出： -> 001-xxxx.png (1579KB)
        # 或者是输出目录： Output: tmp/gemini-image-gen-xxxx
        # 我们寻找以 .png 结尾的文件名行
        match = re.search(r"->\s+(.*\.png)", output)
        dir_match = re.search(r"Output:\s+(tmp/gemini-image-gen-[\d-]+)", output)
        
        if not match or not dir_match:
            return {"error": "无法从脚本输出中解析图片路径", "debug": output}

        filename = match.group(1).strip()
        rel_dir = dir_match.group(1).strip()
        src_file = os.path.join(rel_dir, filename)

        if not os.path.exists(src_file):
            return {"error": f"找到路径但文件不存在: {src_file}"}
        
        # 3. 部署至 1Panel
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            
        dest_file = os.path.join(OUTPUT_DIR, filename)
        shutil.copy2(src_file, dest_file)

        # 4. 返回
        return {
            "success": True,
            "url": f"{BASE_URL}/{filename}",
            "prompt": prompt,
            "filename": filename
        }

    except subprocess.CalledProcessError as e:
        return {"error": f"绘图脚本执行失败: {e.stderr}"}
    except Exception as e:
        return {"error": f"处理异常: {str(e)}"}

if __name__ == "__main__":
    try:
        raw_input = sys.argv[1] if len(sys.argv) > 1 else "{}"
        args = json.loads(raw_input)
        print(json.dumps(main(args)))
    except Exception as e:
        print(json.dumps({"error": str(e)}))