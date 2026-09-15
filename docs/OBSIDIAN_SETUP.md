# Obsidian 配置

## 第一版不需要额外 Obsidian 插件

核心原因：Obsidian 笔记本质上是本地 Markdown 文件。Codex 直接读取指定主题文件夹即可完成搜索、生成 `[[双向链接]]` 和写入 Markdown。

第一版**不强依赖**：

- Local REST API
- MCP
- Dataview
- Obsidian Git 社区插件

这些都可以以后按需求增加。

## 推荐 Vault 结构

```text
ResearchVault/
└── Research/
    ├── Hyperspectral Imaging/
    │   ├── Papers/
    │   ├── Concepts/
    │   ├── Methods/
    │   └── MOC.md
    └── Other Topic/
```

不要一开始就建很多空目录。Datasets、Metrics 等只有实际需要时再增加。

## 搜索范围

Skill 只读取当前论文状态绑定的主题目录。例如当前主题是：

```text
Research/Hyperspectral Imaging/
```

则不得默认扫描 `Research/` 其他主题或整个 Vault。

## 节点粒度

值得单独建节点：

- 可跨论文复用的理论
- 方法/算法
- 重要实验方法
- 常用评价指标
- 重要数据集/实验平台
- 可复用研究问题

通常不值得单独建节点：

- 论文里只出现一次的普通术语
- 作者自定义模块名称
- 一次性参数细节

## Properties / YAML

是可选增强，不默认启用。

用途：

- 按 citekey、年份、方法、数据集检索
- 后续配合 Properties / Dataview
- 管理阅读状态

在每次知识库整理前，Skill 必须先解释用途，再问你是否启用。

## 文件名

每个研究主题独立编号：

```text
001-Shortened English Title.md
002-Another English Title.md
```

英文原题适度缩短；citekey 放到元数据，不强行加入文件名。

## 写入安全

知识库整理流程必须是：

```text
读取指定主题 → 生成提案 → 用户审阅 → 用户确认 → 写入 → Git diff/更新记录
```

不允许直接生成最终主笔记并悄悄写入 Vault。

## 版本回退

最通用方案是直接让 Vault 使用 Git。无需 Obsidian Git 插件也能工作。

如果你未来使用 Obsidian Sync，它自身也有版本历史，但本项目仍建议保留 Git 作为清晰的变更审计层。
