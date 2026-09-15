# 示例工程：从待读到知识库

本示例使用**虚构论文**，只演示工作流，不提供任何真实实验结论。

假设：

- 研究主题：`Example Imaging`
- Zotero citekey：`demo2026imaging`
- Zotero item key：`ABCD1234`
- 论文题目：`A Demonstration Method for Engineering Imaging`

## Step 1：创建主题

先预览：

```powershell
python scripts\create_topic.py `
  --workspace "D:\Research\research-workspace" `
  --topic "Example Imaging" `
  --obsidian-vault "D:\Obsidian\ResearchVault" `
  --research-root "Research" `
  --create-obsidian-dirs
```

确认后加 `--apply`。

## Step 2：Zotero 入库

在 Zotero：

- 放入 `Example Imaging` Collection
- 附 PDF
- Tag：`状态/待读`
- BBT citekey：`demo2026imaging`

## Step 3：筛选

对 Codex：

> 筛选论文 demo2026imaging

预期：只在对话里得到导读、推荐档位、重点章节/页码、20 分钟阅读路线。

## Step 4：精读

> 精读论文 demo2026imaging

预期工作区生成类似：

```text
deep-reading/Example-Imaging/demo2026imaging/deep-reading.md
```

此时 Zotero 建议状态：`状态/整理`。

## Step 5：自己补知识

你在 Obsidian 的指定主题目录里补充自己的知识点和理解。

## Step 6：整理知识库

> 整理知识库 demo2026imaging

Skill 先读取当前主题知识，自动串联一部分，再针对真正需要你判断的地方逐个提问。

输出：

```text
drafts/Example-Imaging/demo2026imaging/knowledge-update-proposal.md
```

不会直接写入 Vault。

## Step 7：确认并完成

你确认提案后：

> 完成论文笔记 demo2026imaging

最终主题内可能形成：

```text
Papers/001-A Demonstration Method for Engineering Imaging.md
Concepts/Some Reusable Concept.md
Methods/Some Reusable Method.md
MOC.md
```

最后建议 Zotero `状态/已读`。
