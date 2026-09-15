# 模块 05：Obsidian 集成

## 原则

第一版不依赖 Obsidian Local REST API/MCP。Codex 直接读写 Vault 内 Markdown 文件，但写入仍需用户确认。

## Vault 范围

只读取当前论文绑定的研究主题目录，例如：

```text
Research/Hyperspectral Imaging/
```

不扫描整个 Vault。

## 推荐结构

```text
<主题>/
├── Papers/
├── Concepts/
├── Methods/
├── Datasets/       # 可选
├── Metrics/        # 可选
└── MOC.md
```

不要强行创建所有目录；按实际需要控制粒度。

## 双向链接

优先连接跨论文可复用知识：理论、方法、指标、数据集、研究问题。作者自定义模块名或一次性细节通常留在论文主笔记。

## 主笔记文件名

主题内独立编号：

`NNN-Shortened English Title.md`

例如：`003-Spectral-Spatial Transformer.md`

## 更新策略

以 citekey 识别同一论文：

- 已存在 → 先生成更新提案
- 不创建 `v2` / `final-final`
- 确认后更新原文件
- 在底部添加简短更新历史

## Properties

可选，不默认强制。整理前说明并询问。

推荐字段：

- type
- title
- authors
- year
- venue
- doi
- citekey
- topic
- paper_type
- reading_status
- methods
- datasets
- keywords
- zotero_item_key
- created
- updated
