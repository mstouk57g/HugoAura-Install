"""
自动更新版本信息脚本
从HugoAura GitHub仓库获取最新的版本信息并更新versions.json文件
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import requests


def get_github_releases(repo: str, token: str) -> List[Dict]:
    """
    从GitHub API获取仓库的所有releases
    
    Args:
        repo: 仓库名称 (owner/repo)
        token: GitHub访问令牌
        
    Returns:
        releases列表
    """
    url = f"https://api.github.com/repos/{repo}/releases"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ 获取GitHub releases失败: {e}")
        sys.exit(1)


def process_releases(releases_data: List[Dict]) -> Dict:
    """
    处理GitHub releases数据, 分类为releases和prereleases
    
    Args:
        releases_data: GitHub API返回的releases数据
        
    Returns:
        处理后的版本信息字典
    """
    releases = []
    prereleases = []
    
    for release in releases_data:
        # 跳过草稿版本
        if release.get("draft", False):
            continue
            
        version_info = {
            "tag": release["tag_name"],
            "name": f"[{'Pre' if release['prerelease'] else 'Rel'}] {release['name'] or release['tag_name']}",
            "type": "prerelease" if release["prerelease"] else "release",
            "published_at": release.get("published_at"),
            "download_url": get_download_url(release)
        }
        
        if release["prerelease"]:
            prereleases.append(version_info)
        else:
            releases.append(version_info)
    
    # CI 构建版本 (固定)
    ci_builds = [
        {
            "tag": "vAutoBuild",
            "name": "[CI] HugoAura Auto Build Release",
            "type": "ci"
        }
    ]
    
    return {
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "releases": releases,
        "prereleases": prereleases,
        "ci_builds": ci_builds
    }


def get_download_url(release: Dict) -> str:
    """
    从release信息中提取下载URL
    
    Args:
        release: GitHub release信息
        
    Returns:
        下载URL
    """
    assets = release.get("assets", [])
    
    # 寻找 .asar 文件
    for asset in assets:
        if asset["name"].endswith(".asar"):
            return asset["browser_download_url"]
    
    # 如果没有 .asar 文件, 返回第一个资源的下载链接
    if assets:
        return assets[0]["browser_download_url"]
        
    return ""


def update_versions_file(versions_data: Dict, file_path: Path) -> bool:
    """
    更新 versions.json 文件
    
    Args:
        versions_data: 新的版本数据
        file_path: 版本文件路径
        
    Returns:
        是否有更新
    """
    # 检查文件是否存在以及内容是否有变化
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            
            # 比较版本数据 (忽略 last_updated 字段)
            existing_copy = existing_data.copy()
            new_copy = versions_data.copy()
            existing_copy.pop('last_updated', None)
            new_copy.pop('last_updated', None)
            
            if existing_copy == new_copy:
                print("ℹ️ 版本信息无变化, 跳过更新")
                return False
        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️ 读取现有版本文件失败: {e}")
    
    # 写入新的版本数据
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(versions_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 版本信息已更新: {file_path}")
        return True
    except Exception as e:
        print(f"❌ 写入版本文件失败: {e}")
        sys.exit(1)


def main():
    """主函数"""
    # 配置
    HUGOAURA_REPO = "HugoAura/Seewo-HugoAura"
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        print("❌ 未找到 GITHUB_TOKEN 环境变量")
        sys.exit(1)
    
    # 获取脚本所在目录的项目根目录
    script_dir = Path(__file__)
    project_root = script_dir.parent
    versions_file = project_root / "src" / "app" / "public" / "versions.json"
    
    print(f"🚀 开始更新版本信息...")
    print(f"📦 目标仓库: {HUGOAURA_REPO}")
    print(f"📄 版本文件: {versions_file}")
    
    # 获取GitHub releases
    print("📡 正在获取 GitHub releases...")
    releases_data = get_github_releases(HUGOAURA_REPO, github_token)
    print(f"✅ 获取到 {len(releases_data)} 个版本")
    
    # 处理版本数据
    print("🔄 正在处理版本数据...")
    versions_info = process_releases(releases_data)
    
    print(f"📊 版本统计:")
    print(f"  - 发行版: {len(versions_info['releases'])}")
    print(f"  - 预发行版: {len(versions_info['prereleases'])}")
    print(f"  - CI构建版: {len(versions_info['ci_builds'])}")
    
    # 更新版本文件
    if update_versions_file(versions_info, versions_file):
        print("🎉 版本信息更新完成!")
    else:
        print("ℹ️ 无需更新版本信息")


if __name__ == "__main__":
    main()
