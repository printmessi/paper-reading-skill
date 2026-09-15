# 在 Codex 中使用本 Skill

## Skill 结构

OpenAI Skill 的核心是一个带 `name` 和 `description` frontmatter 的 `SKILL.md`，并可在同一目录带模板、文档和脚本。本工程已经按这个结构组织。

## 推荐方式 A：作为本地 Skill 目录

保留整个 `paper-reading-skill` 目录，不要只复制 `SKILL.md`，因为主文件会引用 `modules/`、`templates/`、`scripts/` 和 `docs/`。

在你的 Codex 环境中把该目录放入当前版本支持的个人或项目 Skill 位置。由于 Codex 的 Skill 发现位置/界面可能随版本变化，安装后应在新会话里确认它是否出现在可用 Skills 列表。

如果没有自动发现：

1. 参考根目录 `AGENTS.example.md`；
2. 在当前项目的 `AGENTS.md` 中加入 Skill 名称、用途和 `SKILL.md` 绝对路径；
3. 或在当前会话明确要求 Codex 读取该 `SKILL.md`。

## 推荐方式 B：上传 Skill Bundle

如果你的 OpenAI/Codex 环境支持项目 Skills 上传，可以直接使用本工程 ZIP 作为 Skill bundle。OpenAI Skills API 支持以目录文件或 ZIP 创建 Skill。

官方 Skills 介绍：

`https://openai.com/academy/skills/`

API 参考：

`https://developers.openai.com/api/reference/python/resources/skills/methods/create`

## 安装后测试

在 Codex 里输入：

> 使用帮助

预期：Skill 应先介绍 Zotero / Obsidian / Codex 的分工和首次初始化流程，而不是立即要求上传论文。

然后输入：

> 初始化论文阅读工作区

Skill 应先做环境检查和路径规划，不自动安装任何软件。
