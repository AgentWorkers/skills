#!/usr/bin/env python3
"""
Translate SKILL.md files from upstream skills repository.

This script:
1. Downloads upstream main.zip from GitHub
2. Extracts archive to .cache/skills-main/skills
3. Scans for all SKILL.md files
4. Checks if content is already in Chinese
5. Sends non-Chinese files to the translation service
6. Updates the files with translated content
7. Replaces ./skills with translated directory
8. Cleans up intermediate files

Features:
- Downloads and extracts upstream archive automatically
- Skips files that are already in Chinese
- Uses translation cache for efficiency
- Supports dry-run mode
- Supports skip-download and skip-replace options
"""

import argparse
import base64
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
import threading
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import os

import httpx


@dataclass
class TranslationTask:
    """需要翻译的文件任务"""

    file_path: str  # 远程文件路径（用于日志）
    local_path: Path  # 本地保存路径
    content: str  # 文件内容
    content_hash: str  # 内容 hash


# Allow overriding via environment variables for GitHub Actions
# UPSTREAM_REPO_URL: Override the upstream GitHub repository URL
upstream_repo_lastest_archive = os.environ.get(
    "UPSTREAM_REPO_URL",
    "https://github.com/openclaw/skills/archive/refs/heads/main.zip",
)

# Cache directory paths
cache_dir = Path(".cache")
archive_path = cache_dir / "main.zip"
target_skills_dir = Path("skills")

# Incremental sync constants
SYNC_COMMIT_ID_FILE = Path("SYNC_COMMIT_ID")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO", "openclaw/skills")
UPSTREAM_REPO_URL = f"https://github.com/{UPSTREAM_REPO}"

# Dynamically determined after extraction
extracted_dir: Optional[Path] = None
source_skills_dir: Optional[Path] = None

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


def get_latest_commit_id(
    repo_url: str = "https://github.com/openclaw/skills", branch_name: str = "main"
):
    """
    获取远程仓库指定分支的最新 Commit ID
    """
    # 构造 git ls-remote 命令
    # 格式: git ls-remote <repo_url> refs/heads/<branch_name>
    command = ["git", "ls-remote", repo_url, f"refs/heads/{branch_name}"]

    try:
        # 执行命令
        # capture_output=True 表示捕获标准输出和标准错误
        # text=True 表示将输出解码为字符串 (Python 3.7+)
        # check=True 如果命令返回非零状态码则抛出异常
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # 标准输出通常格式为: "<commit_id>\t<ref_name>"
        # 例如: "a1b2c3d4e5f...\trefs/heads/main\n"
        output = result.stdout.strip()

        if not output:
            print(f"未找到分支: {branch_name}")
            return None

        # 按制表符分割，取第一部分即为 Commit ID
        commit_id = output.split("\t")[0]
        return commit_id

    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        print(f"错误信息: {e.stderr}")
        return None
    except FileNotFoundError:
        print("错误: 系统中未找到 git 命令，请确保已安装 Git 并添加到环境变量。")
        return None


def get_gitdiffs() -> str:
    """
    下载 gitdiffs 工具到 .cache/bin 目录

    Returns:
        gitdiffs 可执行文件的路径
    """
    gitdiffs_dir = cache_dir / "bin"
    gitdiffs_dir.mkdir(parents=True, exist_ok=True)
    gitdiffs_path = gitdiffs_dir / "gitdiffs"

    # 如果已存在，直接返回
    if gitdiffs_path.exists():
        return str(gitdiffs_path)

    print("📥 Downloading gitdiffs tool...")

    url = "https://github.com/AgentWorkers/gitdiffs/releases/download/v0.1.0/gitdiffs-x86_64-linux.tar.gz"

    for attempt in range(MAX_RETRIES):
        try:
            response = httpx.get(url, follow_redirects=True, timeout=30.0)
            response.raise_for_status()

            # 解压 tar.gz 文件
            with tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz") as tar:
                tar.extractall(gitdiffs_dir)

            print(f"✅ gitdiffs downloaded to: {gitdiffs_path}")
            return str(gitdiffs_path)
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                print(f"⚠️  Download failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
                time.sleep(RETRY_DELAY)
            else:
                print(
                    f"❌ Failed to download gitdiffs after {MAX_RETRIES} attempts: {e}"
                )
                raise


def get_incremental_changes() -> Optional[dict]:
    """
    获取增量变更列表

    Returns:
        包含变更信息的字典，格式：
        {
            "repo": "openclaw/skills",
            "base": "commit_id",
            "head": "commit_id",
            "files": [{"status": "ADD|DEL|MODIFY", "path": "..."}, ...]
        }
        如果失败返回 None
    """
    # 检查 SYNC_COMMIT_ID 文件是否存在
    if not SYNC_COMMIT_ID_FILE.exists():
        print("❌ SYNC_COMMIT_ID file not found. Please use --full for initial sync.")
        return None

    sync_commit_id = SYNC_COMMIT_ID_FILE.read_text().strip()
    latest_commit_id = get_latest_commit_id(UPSTREAM_REPO_URL)

    if not latest_commit_id:
        print("❌ Failed to get latest commit ID")
        return None

    if sync_commit_id == latest_commit_id:
        print("✅ Already up to date, no changes to sync")
        sys.exit(0)

    print(f"📌 Syncing from {sync_commit_id[:8]} to {latest_commit_id[:8]}")

    # 获取 gitdiffs 工具
    gitdiffs_path = get_gitdiffs()

    # 调用 gitdiffs 获取差异
    cmd = [gitdiffs_path, UPSTREAM_REPO_URL, sync_commit_id, latest_commit_id]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        changes = json.loads(result.stdout.strip())
        print(f"📋 Found {len(changes.get('files', []))} changed files")
        return changes
    except subprocess.CalledProcessError as e:
        print(f"❌ gitdiffs command failed: {e}")
        print(f"   stderr: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse gitdiffs output: {e}")
        return None


def download_single_file(file_path: str, commit: str) -> Optional[bytes]:
    """
    从 GitHub 下载单个文件

    Args:
        file_path: 文件路径（如 skills/xxx/SKILL.md）
        commit: commit ID

    Returns:
        文件内容（bytes），失败返回 None
    """
    # 使用 GitHub raw API
    url = f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/{commit}/{file_path}"

    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    for attempt in range(MAX_RETRIES):
        try:
            response = httpx.get(
                url, headers=headers, timeout=30.0, follow_redirects=True
            )
            response.raise_for_status()
            return response.content
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                print(f"⚠️  File not found: {file_path}")
                return None
            if attempt < MAX_RETRIES - 1:
                print(
                    f"⚠️  Download failed (attempt {attempt + 1}/{MAX_RETRIES}): HTTP {e.response.status_code}"
                )
                time.sleep(RETRY_DELAY)
            else:
                print(f"❌ Failed to download {file_path} after {MAX_RETRIES} attempts")
                return None
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                print(f"⚠️  Download failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
                time.sleep(RETRY_DELAY)
            else:
                print(
                    f"❌ Failed to download {file_path} after {MAX_RETRIES} attempts: {e}"
                )
                return None

    return None


def process_single_add_del_task(
    file_info: dict,
    head_commit: str,
    stats: dict,
    translation_tasks: list,
):
    """
    处理单个 ADD/DEL 任务（串行执行）

    Args:
        file_info: 文件信息字典，包含 status 和 path
        head_commit: 最新 commit ID
        stats: 统计信息字典
        translation_tasks: 翻译任务列表
    """
    status = file_info.get("status")
    file_path = file_info.get("path")

    # 只处理 skills 目录下的文件
    if not file_path.startswith("skills/"):
        return

    # 本地路径（去掉 skills/ 前缀）
    local_path = target_skills_dir / file_path[7:]

    if status == "DEL":
        # 删除文件
        if local_path.exists():
            local_path.unlink()
            print(f"🗑️  Deleted: {file_path}")
            stats["deleted"] += 1
        else:
            print(f"⚠️  File not found for deletion: {file_path}")
    else:
        # ADD 或 MODIFY - 下载文件
        print(f"📥 Downloading: {file_path}")

        content = download_single_file(file_path, head_commit)
        if content is None:
            stats["failed"] += 1
            return

        # 创建父目录
        local_path.parent.mkdir(parents=True, exist_ok=True)

        # 判断是否需要翻译
        if file_path.endswith("SKILL.md"):
            # 需要翻译的文件
            try:
                text_content = content.decode("utf-8")
            except UnicodeDecodeError as e:
                print(f"⚠️  Encoding error for {file_path}: {e}")
                stats["failed"] += 1
                return

            # 检查是否已经是中文
            if is_chinese_content(text_content):
                local_path.write_bytes(content)
                print(f"⏭️  Already Chinese: {file_path}")
                stats["skipped_chinese"] += 1
                return

            # 先保存源文件到本地（保证即使翻译失败也有源文件）
            local_path.write_bytes(content)

            # 加入翻译任务列表
            content_hash = compute_hash(text_content)

            task = TranslationTask(
                file_path=file_path,
                local_path=local_path,
                content=text_content,
                content_hash=content_hash,
            )
            translation_tasks.append(task)
            print(f"📋 Queued for translation: {file_path}")
        else:
            # 其他文件直接保存
            local_path.write_bytes(content)
            print(f"✅ Saved: {file_path}")
            stats["downloaded"] += 1


def execute_add_del_phase(
    config: TranslateConfig, changes: dict
) -> tuple[dict, list[TranslationTask]]:
    """
    第一阶段：串行执行 ADD/DEL 任务，收集翻译任务列表

    Args:
        config: 翻译配置
        changes: 变更信息字典

    Returns:
        Tuple of (stats, translation_tasks)
    """
    stats = {
        "total_changes": len(changes.get("files", [])),
        "downloaded": 0,
        "translated": 0,
        "deleted": 0,
        "skipped_chinese": 0,
        "failed": 0,
    }
    translation_tasks: list[TranslationTask] = []

    if not changes.get("files"):
        return stats, translation_tasks

    head_commit = changes.get("head", "main")
    files = changes.get("files", [])

    print(f"🔧 Phase 1: Executing ADD/DEL tasks (sequential)")
    print(f"📋 Total files to process: {len(files)}")

    for file_info in files:
        try:
            process_single_add_del_task(
                file_info, head_commit, stats, translation_tasks
            )
        except Exception as e:
            print(f"❌ Unexpected error for {file_info.get('path')}: {e}")
            stats["failed"] += 1

    print(f"✅ Phase 1 complete. Translation tasks queued: {len(translation_tasks)}")
    return stats, translation_tasks


def process_single_translation(
    config: TranslateConfig,
    task: TranslationTask,
    stats: dict,
    stats_lock: threading.Lock,
    index: int,
    total: int,
):
    """
    处理单个翻译任务（用于并发执行）

    Args:
        config: 翻译配置
        task: 翻译任务
        stats: 统计信息字典
        stats_lock: 统计信息锁
        index: 当前索引
        total: 总数
    """
    print(f"[{index}/{total}] Translating: {task.file_path}")

    relative_path = str(task.local_path.relative_to(target_skills_dir))

    result = translate_file(config, task.content, relative_path, task.content_hash)

    if result:
        translated_content, translated_hash, metadata = result
        task.local_path.write_text(translated_content, encoding="utf-8")

        with stats_lock:
            if metadata.get("cached", False):
                stats["cached"] += 1
                print(f"[{index}/{total}] ✅ Translated (cached): {task.file_path}")
            else:
                stats["translated"] += 1
                print(f"[{index}/{total}] ✅ Translated: {task.file_path}")
    else:
        # 翻译失败，保存原文件
        task.local_path.write_text(task.content, encoding="utf-8")
        print(f"[{index}/{total}] ⚠️  Translation failed, saved original: {task.file_path}")
        with stats_lock:
            stats["failed"] += 1


def translate_collected_phase(
    config: TranslateConfig, translation_tasks: list[TranslationTask], max_workers: int = 5
) -> dict:
    """
    第二阶段：并发翻译收集到的文件

    Args:
        config: 翻译配置
        translation_tasks: 翻译任务列表
        max_workers: 最大并发数

    Returns:
        统计信息字典
    """
    stats = {
        "translated": 0,
        "cached": 0,
        "failed": 0,
    }
    stats_lock = threading.Lock()

    if not translation_tasks:
        return stats

    total = len(translation_tasks)
    print(f"\n🔧 Phase 2: Translating {total} files with {max_workers} workers")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                process_single_translation,
                config,
                task,
                stats,
                stats_lock,
                i,
                total,
            ): task
            for i, task in enumerate(translation_tasks, 1)
        }

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                task = futures[future]
                print(f"❌ Unexpected error translating {task.file_path}: {e}")
                with stats_lock:
                    stats["failed"] += 1

    print(f"✅ Phase 2 complete. Translated: {stats['translated']}, Cached: {stats['cached']}, Failed: {stats['failed']}")
    return stats


def process_incremental_changes(config: TranslateConfig, changes: dict) -> dict:
    """
    处理增量变更（两阶段）

    第一阶段：串行执行 ADD/DEL 任务，收集翻译任务列表
    第二阶段：并发翻译收集到的文件

    Args:
        config: 翻译配置
        changes: 变更信息字典

    Returns:
        统计信息字典
    """
    # 第一阶段：串行执行 ADD/DEL 任务
    stats, translation_tasks = execute_add_del_phase(config, changes)

    # 第二阶段：并发翻译（固定 5 个并发）
    if translation_tasks:
        translation_stats = translate_collected_phase(
            config, translation_tasks, max_workers=5
        )
        # 合并翻译统计
        stats["translated"] = translation_stats.get("translated", 0)
        stats["cached"] = translation_stats.get("cached", 0)
        # 翻译失败计入总失败数
        stats["failed"] += translation_stats.get("failed", 0)
    else:
        stats["cached"] = 0

    return stats


def download_upstream_archive(skip_download: bool = False) -> bool:
    """
    Download the upstream archive to cache directory.

    Args:
        skip_download: If True, skip download and use existing archive.

    Returns:
        True if archive exists (downloaded or already present), False otherwise.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)

    if skip_download and archive_path.exists():
        print(f"📦 Using existing archive: {archive_path}")
        return True

    if skip_download and not archive_path.exists():
        print(f"❌ Archive not found: {archive_path}")
        return False

    print("⬇️  Downloading upstream archive...")
    print(f"   URL: {upstream_repo_lastest_archive}")

    try:
        with httpx.Client(timeout=300.0, follow_redirects=True) as client:
            response = client.get(upstream_repo_lastest_archive)
            response.raise_for_status()

            archive_path.write_bytes(response.content)
            print(f"✅ Downloaded to: {archive_path}")
            return True
    except Exception as e:
        print(f"❌ Failed to download archive: {e}")
        return False


def extract_archive() -> bool:
    """
    Extract the downloaded archive to cache directory.
    Dynamically detects the extracted directory name from the zip file.

    Returns:
        True if extraction successful, False otherwise.
    """
    global extracted_dir, source_skills_dir

    if not archive_path.exists():
        print(f"❌ Archive not found: {archive_path}")
        return False

    print("📦 Extracting archive...")

    try:
        with zipfile.ZipFile(archive_path, "r") as zf:
            # Detect the root directory name from the zip file
            # GitHub archives have format: {repo_name}-{ref}/
            namelist = zf.namelist()
            if not namelist:
                print("❌ Empty archive")
                return False

            # Get the root directory name (first path component)
            root_dir = namelist[0].split("/")[0]
            if not root_dir:
                print("❌ Could not determine archive root directory")
                return False

            zf.extractall(cache_dir)

            # Set global paths based on detected directory
            extracted_dir = cache_dir / root_dir
            source_skills_dir = extracted_dir / "skills"

            if source_skills_dir.exists():
                print(f"✅ Extracted to: {extracted_dir}")
                return True
            else:
                print(f"❌ Skills directory not found in archive: {source_skills_dir}")
                return False
    except zipfile.BadZipFile as e:
        print(f"❌ Invalid zip file: {e}")
        return False
    except Exception as e:
        print(f"❌ Failed to extract archive: {e}")
        return False


def replace_skills_dir() -> bool:
    """
    Replace the target skills directory with the translated source directory.

    Returns:
        True if replacement successful, False otherwise.
    """
    if source_skills_dir is None or not source_skills_dir.exists():
        print(f"❌ Source skills directory not found: {source_skills_dir}")
        return False

    print(f"🔄 Replacing {target_skills_dir} with translated files...")

    try:
        # Remove target directory if it exists
        if target_skills_dir.exists():
            shutil.rmtree(target_skills_dir)

        # Copy source to target
        shutil.copytree(source_skills_dir, target_skills_dir)

        print(f"✅ Replaced {target_skills_dir}")
        return True
    except Exception as e:
        print(f"❌ Failed to replace skills directory: {e}")
        return False


def cleanup_cache():
    """Clean up intermediate files in cache directory."""
    print("🧹 Cleaning up cache...")

    cleaned = []

    if extracted_dir is not None and extracted_dir.exists():
        shutil.rmtree(extracted_dir)
        cleaned.append(str(extracted_dir))

    if archive_path.exists():
        archive_path.unlink()
        cleaned.append(str(archive_path))

    if cleaned:
        print(f"✅ Cleaned up: {', '.join(cleaned)}")
    else:
        print("✅ No cache files to clean")


class TranslateConfig:
    """Configuration for the translation process."""

    def __init__(
        self,
        skills_dir: Optional[str] = None,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        source_language: str = "en",
        target_language: str = "zh-CN",
        max_concurrent: int = 2,
    ):
        self.skills_dir = Path(skills_dir) if skills_dir else None
        # Use environment variable TRANSLATE_API_URL as default if not provided
        self.api_url = (
            api_url or os.environ.get("TRANSLATE_API_URL", "http://127.0.0.1:8080")
        ).rstrip("/")
        # Use environment variable TRANSLATE_API_KEY as default if not provided
        self.api_key = api_key or os.environ.get("TRANSLATE_API_KEY", "")
        self.source_language = source_language
        self.target_language = target_language
        self.max_concurrent = max_concurrent


def compute_hash(content: str) -> str:
    """Compute SHA256 hash of content."""
    return f"sha256:{hashlib.sha256(content.encode('utf-8')).hexdigest()}"


def encode_content(content: str) -> str:
    """Encode content to base64."""
    return base64.b64encode(content.encode("utf-8")).decode("ascii")


def decode_content(encoded: str) -> str:
    """Decode content from base64."""
    return base64.b64decode(encoded.encode("utf-8")).decode("utf-8")


def is_chinese_content(content: str | None) -> bool:
    """
    Check if the content is primarily in Chinese.

    Returns True if the content contains significant Chinese characters.
    Returns False if content is None or empty.
    """
    # Handle None or empty content
    if not content:
        return False

    # Remove code blocks and frontmatter for analysis
    text_content = content

    # Remove YAML frontmatter
    if text_content.startswith("---"):
        parts = text_content.split("---", 2)
        if len(parts) >= 3:
            text_content = parts[2]

    # Remove code blocks
    text_content = re.sub(r"```[\s\S]*?```", "", text_content)

    # Remove inline code
    text_content = re.sub(r"`[^`]+`", "", text_content)

    # Remove URLs
    text_content = re.sub(r"https?://\S+", "", text_content)

    # Remove English words (sequences of ASCII letters)
    text_content = re.sub(r"[a-zA-Z]+", "", text_content)

    # Count Chinese characters (CJK Unified Ideographs) - use processed text_content
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", text_content)

    # Count total text characters (Chinese + ASCII letters + digits) - use processed text_content
    total_text_chars = len(
        re.findall(
            r"[\u4e00-\u9fff\u0030-\u0039\u0041-\u005a\u0061-\u007a]", text_content
        )
    )

    if total_text_chars == 0:
        return False

    chinese_ratio = len(chinese_chars) / total_text_chars

    # If more than 30% Chinese characters, consider it Chinese content
    return chinese_ratio > 0.3


def read_file_safe(path: Path) -> tuple[Optional[str], Optional[str]]:
    """
    Safely read a file with UTF-8 encoding.

    Returns:
        Tuple of (content, error_message). If successful, error_message is None.
        If failed, content is None and error_message contains the error.
    """
    try:
        content = path.read_text(encoding="utf-8")
        return content, None
    except UnicodeDecodeError as e:
        return None, f"UnicodeDecodeError: {e}"
    except Exception as e:
        return None, f"Error: {e}"


def find_skill_files(config: TranslateConfig) -> list[Path]:
    """Find all SKILL.md files in the skills directory."""
    skill_files = []
    for path in config.skills_dir.rglob("SKILL.md"):
        # Skip if in .git directory
        if ".git" in str(path):
            continue
        skill_files.append(path)
    return sorted(skill_files)


def translate_file(
    config: TranslateConfig, content: str, path: str, content_hash: str
) -> Optional[tuple[str, str, dict]]:
    """
    Send a file to the translation service.

    Returns:
        Tuple of (translated_content, translated_hash, metadata) or None on failure
    """
    url = f"{config.api_url}/api/translate"

    payload = {
        "content": encode_content(content),
        "path": path,
        "content_hash": content_hash,
        "options": {
            "source_language": config.source_language,
            "target_language": config.target_language,
        },
    }

    headers = {}
    if config.api_key:
        headers["Authorization"] = f"Bearer {config.api_key}"

    try:
        with httpx.Client(timeout=600.0) as client:
            response = client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            translated_content = decode_content(data["translated_content"])
            translated_hash = data["translated_hash"]
            metadata = data["metadata"]

            return translated_content, translated_hash, metadata
    except httpx.HTTPStatusError as e:
        print(f"❌ Translation failed for {path}: HTTP {e.response.status_code}")
        print(f"   Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"❌ Translation failed for {path}: {str(e)}")
        return None


def write_translated_file(
    config: TranslateConfig, file_path: Path, content: str, metadata: dict
):
    """Write a translated file."""
    # Write the translated content
    file_path.write_text(content, encoding="utf-8")


def process_single_file(
    config: TranslateConfig,
    skill_path: Path,
    index: int,
    total: int,
    stats: dict,
    stats_lock: threading.Lock,
):
    """
    Process a single file: read, check Chinese, translate, write.

    This function is designed to be run in a thread pool.
    """
    relative_path = str(skill_path.relative_to(config.skills_dir))
    print(f"\n[{index}/{total}] Processing: {relative_path}")

    # Read content safely
    content, error = read_file_safe(skill_path)
    if error:
        with stats_lock:
            stats["skipped_encoding"] += 1
        print(f"  ⚠️  Skipped (encoding error: {error})")
        return

    # Type guard: ensure content is not None
    if content is None:
        with stats_lock:
            stats["skipped_encoding"] += 1
        print("  ⚠️  Skipped (empty content)")
        return

    content_hash = compute_hash(content)

    # Check if already Chinese
    if is_chinese_content(content):
        with stats_lock:
            stats["skipped_chinese"] += 1
        print("  ⏭️  Already in Chinese, skipping")
        return

    # Translate
    result = translate_file(config, content, relative_path, content_hash)

    if result:
        translated_content, translated_hash, metadata = result

        # Write to file
        write_translated_file(config, skill_path, translated_content, metadata)

        with stats_lock:
            if metadata.get("cached", False):
                stats["cached"] += 1
                print("  ✅ (cached)")
            else:
                stats["translated"] += 1
                print("  ✅ Translated")
    else:
        with stats_lock:
            stats["failed"] += 1
        print("  ❌ Failed")


def translate_files(config: TranslateConfig, dry_run: bool = False) -> dict:
    """
    Translate all SKILL.md files with concurrent processing.

    Returns:
        Statistics dictionary
    """
    stats = {
        "total_files": 0,
        "translated": 0,
        "cached": 0,
        "failed": 0,
        "skipped_chinese": 0,
        "skipped_unchanged": 0,
        "skipped_encoding": 0,
    }
    stats_lock = threading.Lock()

    # Find all SKILL.md files
    skill_files = find_skill_files(config)
    stats["total_files"] = len(skill_files)

    print(f"\n📂 Found {len(skill_files)} SKILL.md files")
    print(f"🔧 Using {config.max_concurrent} concurrent workers")

    if dry_run:
        print("\n🔍 DRY RUN - Would process the following files:")
        for i, path in enumerate(skill_files, 1):
            relative_path = str(path.relative_to(config.skills_dir))
            content, error = read_file_safe(path)
            if error:
                stats["skipped_encoding"] += 1
                print(f"  {i}. {relative_path} - ⚠️  Skipped (encoding error: {error})")
                continue
            # Type guard: ensure content is not None
            if content is None:
                stats["skipped_encoding"] += 1
                print(f"  {i}. {relative_path} - ⚠️  Skipped (empty content)")
                continue
            is_chinese = is_chinese_content(content)
            status = "🇨🇳 Chinese (skip)" if is_chinese else "🌐 Needs translation"
            print(f"  {i}. {relative_path} - {status}")
        return stats

    # Process files concurrently
    total = len(skill_files)
    with ThreadPoolExecutor(max_workers=config.max_concurrent) as executor:
        futures = {
            executor.submit(
                process_single_file, config, skill_path, i, total, stats, stats_lock
            ): skill_path
            for i, skill_path in enumerate(skill_files, 1)
        }

        # Wait for all tasks to complete
        for future in as_completed(futures):
            # Just wait, errors are handled in process_single_file
            try:
                future.result()
            except Exception as e:
                skill_path = futures[future]
                relative_path = str(skill_path.relative_to(config.skills_dir))
                print(f"  ❌ Unexpected error for {relative_path}: {e}")
                with stats_lock:
                    stats["failed"] += 1

    return stats


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Translate SKILL.md files from upstream skills repository"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Force full sync mode (download entire repository, default is incremental)",
    )
    parser.add_argument(
        "--skills-dir",
        default=None,
        help="Directory containing SKILL.md files to translate (auto-detected from archive if not specified)",
    )
    parser.add_argument(
        "--api-url",
        default=os.environ.get("TRANSLATE_API_URL", "http://127.0.0.1:8080"),
        help="Translation service API URL (or set TRANSLATE_API_URL env var)",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("TRANSLATE_API_KEY", ""),
        help="Translation service API Key (or set TRANSLATE_API_KEY env var)",
    )
    parser.add_argument("--source-language", default="en", help="Source language code")
    parser.add_argument(
        "--target-language", default="zh-CN", help="Target language code"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=10,
        help="Maximum number of concurrent translations (default: 10)",
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip downloading archive, use existing .cache/main.zip",
    )
    parser.add_argument(
        "--skip-replace",
        action="store_true",
        help="Skip replacing ./skills directory after translation",
    )

    args = parser.parse_args()

    # Create config
    config = TranslateConfig(
        skills_dir=args.skills_dir,
        api_url=args.api_url,
        api_key=args.api_key,
        source_language=args.source_language,
        target_language=args.target_language,
        max_concurrent=args.max_concurrent,
    )

    print("=" * 60)
    print("🔄 SKILL.md Translation Script")
    print("=" * 60)
    print(f"API URL: {config.api_url}")
    print(f"Languages: {config.source_language} → {config.target_language}")
    print(f"Mode: {'Full sync' if args.full else 'Incremental'}")
    print("=" * 60)

    # Check if translation service is running (for non-dry-run)
    if not args.dry_run:
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{config.api_url}/api/health")
                response.raise_for_status()
                print("✅ Translation service is running")
        except Exception as e:
            print(f"❌ Translation service is not available: {e}")
            print("   Please start the translation service first:")
            print("   cd skill-translator && python -m server.main")
            sys.exit(1)

    if args.full:
        # Full sync mode
        stats = run_full_sync(config, args)
    else:
        # Incremental sync mode (default)
        stats = run_incremental_sync(config, args)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    print(f"Mode: {'Full sync' if args.full else 'Incremental'}")
    for key, value in stats.items():
        print(f"{key}: {value}")
    print("=" * 60)


def run_full_sync(config: TranslateConfig, args) -> dict:
    """Run full sync mode - download entire repository."""
    # Step 1: Download upstream archive
    if not args.skip_download or not archive_path.exists():
        if not download_upstream_archive(skip_download=args.skip_download):
            sys.exit(1)
    else:
        print(f"📦 Using existing archive: {archive_path}")

    # Step 2: Extract archive
    if not extract_archive():
        sys.exit(1)

    # Update config.skills_dir with the dynamically detected path
    if source_skills_dir is not None:
        config.skills_dir = source_skills_dir

    # Step 3: Check if skills directory exists
    if config.skills_dir is None or not config.skills_dir.exists():
        print(f"\n❌ Skills directory not found: {config.skills_dir}")
        sys.exit(1)

    print(f"📂 Using skills directory: {config.skills_dir}")

    # Step 4: Translate files
    stats = translate_files(config, dry_run=args.dry_run)

    # Step 5: Replace skills directory (if not dry-run and not skip-replace)
    if not args.dry_run and not args.skip_replace:
        if not replace_skills_dir():
            sys.exit(1)

    # Step 6: Clean up cache
    if not args.dry_run:
        cleanup_cache()

    # Step 7: Update SYNC_COMMIT_ID
    if not args.dry_run:
        latest_commit = get_latest_commit_id(UPSTREAM_REPO_URL)
        if latest_commit:
            SYNC_COMMIT_ID_FILE.write_text(latest_commit)
            print(f"📝 Updated SYNC_COMMIT_ID to {latest_commit[:8]}")

    return stats


def run_incremental_sync(config: TranslateConfig, args) -> dict:
    """Run incremental sync mode - only sync changed files."""
    # Get incremental changes
    changes = get_incremental_changes()

    if changes is None:
        print("❌ Failed to get incremental changes")
        sys.exit(1)

    # No changes to sync
    if not changes.get("files"):
        # Update SYNC_COMMIT_ID even when no changes to sync
        if not args.dry_run:
            head_commit = changes.get("head")
            if head_commit:
                SYNC_COMMIT_ID_FILE.write_text(head_commit)
                print(f"📝 Updated SYNC_COMMIT_ID to {head_commit[:8]}")
        return {"total_changes": 0, "message": "Already up to date"}

    # Process changes
    stats = process_incremental_changes(config, changes)

    # Update SYNC_COMMIT_ID
    if not args.dry_run:
        head_commit = changes.get("head")
        if head_commit:
            SYNC_COMMIT_ID_FILE.write_text(head_commit)
            print(f"📝 Updated SYNC_COMMIT_ID to {head_commit[:8]}")

    return stats


if __name__ == "__main__":
    main()
