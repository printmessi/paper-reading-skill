# Zotero + Better BibTeX 配置

## 角色

Zotero 负责：

- 文献元数据
- 原始 PDF
- Collection（研究主题）
- Tag（阅读状态）
- PDF 高亮与批注

Obsidian 才是正式知识库。

## 1. 开启 Zotero Local API

Zotero Desktop 的本地 API 可以让本机脚本通过 HTTP 读取 Zotero 数据，不需要直接访问 SQLite。

在 Zotero：

**Settings → Advanced → Allow other applications on this computer to communicate with Zotero**

本地 API 默认地址：

```text
http://127.0.0.1:23119/api/
```

读取不需要认证；写操作需要 Zotero 本地授权。不要把该端口转发到外网。

官方文档：

`https://www.zotero.org/support/dev/web_api/v3/local_api`

## 2. 安装 Better BibTeX

从 Better BibTeX 官方页面下载最新版 `.xpi`。

Zotero 中：

**Tools → Plugins → 右上角齿轮 → Install Plugin From File…**

选择下载的 `.xpi`。

官方安装说明：

`https://retorque.re/zotero-better-bibtex/installation/`

## 3. Citekey

本工作流把 citekey 当作 Zotero ↔ Obsidian ↔ Codex 的核心文献标识。

Better BibTeX 的优势是：citekey 可稳定生成、可固定、可避免冲突。

建议：

- 第一版先使用 BBT 默认规则；
- 不要频繁修改 citekey 规则；
- 一篇论文进入正式知识库后，尽量不要再改 citekey；
- 如果确实需要改，先检查 Obsidian 中引用。

## 4. Better BibTeX 本地接口

BBT 提供 JSON-RPC：

```text
http://127.0.0.1:23119/better-bibtex/json-rpc
```

本工程的 `zotero_local.py citekey <item_key>` 使用 `item.citationkey` 读取 citekey。

官方文档：

`https://retorque.re/zotero-better-bibtex/exporting/json-rpc/`

## 5. Collection 和 Tag 规则

### Collection = 研究主题

例如：

```text
Hyperspectral Imaging
Optical Imaging
Signal Processing
```

### Tag = 阅读状态

统一：

```text
状态/待读
状态/No
状态/精读
状态/整理
状态/已读
```

流转：

```text
待读 → 精读 → 整理 → 已读
   ↘ No
```

`No` 的含义是“当前不值得继续投入阅读时间”，不是“这篇论文质量差”。

## 6. PDF 原文件保护

本工程遵循：

- Zotero 原 PDF 永不修改；
- 分析前复制到工作区；
- 页码解析、缓存、中间文件只处理副本。

示例：

```powershell
python .\zotero_local.py search "paper title"
python .\zotero_local.py citekey ABCD1234
python .\zotero_local.py copy-pdf ABCD1234 --dest "D:\Research\research-workspace\papers\SomeTopic\SomeCitekey"
```

## 7. Zotero 注释

可读取：高亮、批注、页码等，并在知识库整理时分类成：

- 高亮摘录
- 个人批注
- 待解决问题
- 灵感/联想

示例：

```powershell
python .\zotero_local.py annotations ABCD1234
```

它们是“用户阅读痕迹”，不能当成作者观点。

## 8. 安全更新状态

默认只预览：

```powershell
python .\zotero_status.py ABCD1234 "状态/精读"
```

真正更新必须在用户已经确认后显式执行：

```powershell
python .\zotero_status.py ABCD1234 "状态/精读" --apply --confirm YES
```

Zotero 会进行本地写入授权；脚本使用版本前置条件，避免覆盖并发修改。

## 9. 硬性安全规则

**绝不直接写 `zotero.sqlite`。**

不要为“方便”绕过 Local API/官方写接口。
