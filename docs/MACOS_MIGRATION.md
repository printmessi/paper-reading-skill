# 从 Windows 11 迁移到 macOS

核心 Skill、Markdown 模板和 Python 标准库脚本不依赖 Windows 专属逻辑。

迁移时主要做四件事：

1. 安装 Python 3、Git、Zotero、Obsidian、Codex；
2. 在 Zotero 重新安装/确认 Better BibTeX；
3. 修改工作区与 Vault 路径；
4. 重新检查 Local API 和 Git。

典型路径示例：

```text
/Users/username/Research/research-workspace
/Users/username/Documents/Obsidian/ResearchVault
```

不要把 Windows 的 `C:\...` / `D:\...` 路径写死进 Skill。运行时配置统一放在工作区 `runtime-config.json`。
