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
import re
import shutil
import sys
import threading
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

import os

import httpx


# Allow overriding via environment variables for GitHub Actions
# UPSTREAM_REPO_URL: Override the upstream GitHub repository URL
upstream_repo_lastest_archive = os.environ.get(
    "UPSTREAM_REPO_URL",
    "https://github.com/openclaw/skills/archive/refs/heads/main.zip"
)

# Cache directory paths
cache_dir = Path(".cache")
archive_path = cache_dir / "main.zip"
extracted_dir = cache_dir / "skills-main"
source_skills_dir = extracted_dir / "skills"
target_skills_dir = Path("skills")


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

    Returns:
        True if extraction successful, False otherwise.
    """
    if not archive_path.exists():
        print(f"❌ Archive not found: {archive_path}")
        return False

    print("📦 Extracting archive...")

    try:
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(cache_dir)

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
    if not source_skills_dir.exists():
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

    if extracted_dir.exists():
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
        skills_dir: str = ".cache/skills-main/skills",
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        source_language: str = "en",
        target_language: str = "zh-CN",
        max_concurrent: int = 2,
    ):
        self.skills_dir = Path(skills_dir)
        # Use environment variable TRANSLATE_API_URL as default if not provided
        self.api_url = (api_url or os.environ.get("TRANSLATE_API_URL", "http://127.0.0.1:8080")).rstrip("/")
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
        "--skills-dir",
        default=".cache/skills-main/skills",
        help="Directory containing SKILL.md files to translate",
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
        help="Maximum number of concurrent translations (default: 2)",
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
    print(f"Skills Dir: {config.skills_dir}")
    print(f"API URL: {config.api_url}")
    print(f"Languages: {config.source_language} → {config.target_language}")
    print("=" * 60)

    # Step 1: Download upstream archive
    if not args.skip_download or not archive_path.exists():
        if not download_upstream_archive(skip_download=args.skip_download):
            sys.exit(1)
    else:
        print(f"📦 Using existing archive: {archive_path}")

    # Step 2: Extract archive
    if not extract_archive():
        sys.exit(1)

    # Step 3: Check if skills directory exists
    if not config.skills_dir.exists():
        print(f"\n❌ Skills directory not found: {config.skills_dir}")
        sys.exit(1)

    # Step 4: Check if translation service is running
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

    # Step 5: Translate files
    stats = translate_files(config, dry_run=args.dry_run)

    # Step 6: Replace skills directory (if not dry-run and not skip-replace)
    if not args.dry_run and not args.skip_replace:
        if not replace_skills_dir():
            sys.exit(1)

    # Step 7: Clean up cache
    if not args.dry_run:
        cleanup_cache()

    # Print summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    print(f"Total files: {stats['total_files']}")
    print(f"Translated: {stats['translated']}")
    print(f"Cached: {stats['cached']}")
    print(f"Skipped (Chinese): {stats['skipped_chinese']}")
    print(f"Skipped (Encoding error): {stats['skipped_encoding']}")
    print(f"Failed: {stats['failed']}")
    print("=" * 60)

    # Note: We don't exit with error code when there are failures,
    # as some translation failures (like HTTP 413) are acceptable.
    # The summary still reports failures for visibility.


if __name__ == "__main__":
    main()
