# Windows 11 安装与初始化

本教程采用保守策略：**只检查和引导，不自动安装软件，不自动修改系统环境变量，不自动改 Zotero/Obsidian 配置。**

## 1. 安装基础软件

请手动确认已安装：

- Python 3（建议较新的稳定版）
- Git
- Zotero Desktop
- Obsidian
- Codex

在 PowerShell 中检查：

```powershell
python --version
git --version
```

如果命令不存在，请从各自官方渠道安装，再重新打开终端。

## 2. 检查 Skill 工程

解压本工程后，目录中应至少有：

```text
SKILL.md
README.md
modules/
templates/
scripts/
docs/
```

Codex 的 Skill 发现方式可能随版本变化。最稳妥的原则是：

1. 把整个目录作为一个 Skill 目录保留；
2. 确保 `SKILL.md` 的 `name` / `description` frontmatter 可被发现；
3. 如果当前 Codex 没自动发现，可在项目 `AGENTS.md` 中参考 `AGENTS.example.md` 增加该 Skill 路径；
4. 或在 Codex 会话中明确要求读取本目录的 `SKILL.md`。

## 3. 只做环境检查

在本工程 `scripts` 目录运行：

```powershell
python .\init_workspace.py --check-only
```

它只会输出：

- Python 版本
- Git 是否存在
- 常见 Zotero / Obsidian 安装位置是否可见

不会安装或修改任何内容。

## 4. 规划工作区

推荐把工作区和 Obsidian Vault 分开，例如：

```text
D:\Research\research-workspace
D:\Obsidian\ResearchVault
```

工作区保存 PDF 副本、精读稿、状态和草稿；Vault 只保存最终确认知识。

## 5. 预览初始化

```powershell
python .\init_workspace.py `
  --workspace "D:\Research\research-workspace" `
  --obsidian-vault "D:\Obsidian\ResearchVault" `
  --research-root "Research" `
  --init-git
```

没有 `--apply` 时只预览。

确认后：

```powershell
python .\init_workspace.py `
  --workspace "D:\Research\research-workspace" `
  --obsidian-vault "D:\Obsidian\ResearchVault" `
  --research-root "Research" `
  --init-git `
  --apply
```

生成：

```text
research-workspace/
├── topics/
├── papers/
├── deep-reading/
├── drafts/
├── state/
├── cache/
├── no-records/
├── logs/
├── runtime-config.json
└── .gitignore
```

## 6. 配置 Zotero

继续阅读 `ZOTERO_SETUP.md`。

## 7. 配置 Obsidian

继续阅读 `OBSIDIAN_SETUP.md`。

## 8. 创建第一个研究主题

先预览：

```powershell
python .\create_topic.py `
  --workspace "D:\Research\research-workspace" `
  --topic "Hyperspectral Imaging" `
  --obsidian-vault "D:\Obsidian\ResearchVault" `
  --research-root "Research" `
  --create-obsidian-dirs
```

确认后加：

```powershell
--apply
```

## 9. Git 审计

工作区初始化后建议：

```powershell
cd D:\Research\research-workspace
git status
git add .
git commit -m "Initialize paper reading workspace"
```

`.gitignore` 默认排除 PDF、缓存和日志。正式修改 Obsidian 前，也建议先在 Vault 的 Git 仓库中 `git status` / `git diff`。
