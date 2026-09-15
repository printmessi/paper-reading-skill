# 常见问题

## Zotero Local API 返回 403

检查 Zotero：Settings → Advanced → 允许本机其他应用通信。

## Better BibTeX citekey 读不到

1. 确认 BBT 已安装并启用；
2. 运行 `python zotero_local.py check`；
3. 如果仍不可用，暂时使用 Zotero item key，并明确写“citekey 暂无”，不要伪造。

## Zotero 条目没有 PDF

停止主论文分析。先把 PDF 加入 Zotero。

## PDF 是扫描版

允许有限分析，但章节/公式/图表/页码无法确认的必须标 `待核验`。建议换可搜索文本 PDF。

## Obsidian 没有被自动扫描

这是设计使然。必须给出当前研究主题目录，避免扫描整个 Vault。

## Zotero 状态写入失败 412

说明条目在读取后发生了版本变化。重新读取条目并重新生成修改计划，不能强行覆盖。

## Skill 没被 Codex 自动识别

参考 `AGENTS.example.md` 把 Skill 名称、用途和 `SKILL.md` 路径放到当前项目指令中，或者在会话中明确要求读取该 `SKILL.md`。
