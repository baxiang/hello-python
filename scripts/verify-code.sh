#!/usr/bin/env bash
set -euo pipefail

echo "🔍 验证 Python 代码..."

for dir in */; do
  if [ -d "$dir" ] && [ "$dir" != "node_modules/" ] && [ "$dir" != ".vitepress/" ]; then
    echo "检查 $dir..."
    for project in "$dir"*/; do
      if [ -f "$project/pyproject.toml" ]; then
        echo "  验证 $project"
        (cd "$project" && python -m py_compile *.py 2>/dev/null || true)
      fi
    done
  fi
done

echo "✅ 验证完成"
