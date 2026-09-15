# 模块 04：Zotero 集成

## 定位

Zotero 只负责文献资产：元数据、PDF、Collection、Tag、注释。知识沉淀放 Obsidian。

## 默认入口

优先通过 citekey 或标题找到 Zotero 条目。若 Zotero 没有 PDF，提醒用户添加/上传 PDF，不自行搜主论文全文。

## Better BibTeX

Better BibTeX 提供稳定 citekey。优先通过其本地 JSON-RPC `item.citationkey` 获取 item key 对应 citekey；若 BBT 不可用，明确提示并暂时使用 Zotero item key，不能伪造 citekey。

## PDF

- Zotero 原始 PDF 永不修改。
- 通过 Local API 获取附件路径后复制到工作区临时目录。
- 所有解析、缓存、中间文件都针对副本。

## 注释

可读取并分类：

- 高亮摘录
- 个人批注
- 待解决问题
- 灵感/联想

它们属于用户阅读痕迹，不等同于论文作者观点。

## 研究主题和状态

- Collection：研究主题
- Tag：阅读状态

统一状态：

- `状态/待读`
- `状态/No`
- `状态/精读`
- `状态/整理`
- `状态/已读`

推荐流转：

`待读 → 精读 → 整理 → 已读`

若快速筛选不值得继续：`待读 → No`

## 修改策略

Skill 可以提出：状态、标签、Collection 整理建议。

但实际修改必须满足：

1. 用户明确下达“更新 Zotero …”；
2. 先展示计划修改内容；
3. 用户确认；
4. 通过 Zotero Local API / 支持授权的接口写入；
5. 不直接写 `zotero.sqlite`。

## No 论文

保留工作区简短筛选记录，不进入 Obsidian。Zotero 保留 `状态/No`，可附极简备注。
