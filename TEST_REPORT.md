# Test Report

## 已测试

使用 Python `unittest`：

- 工作区初始化
- 研究主题创建
- 主题内编号扫描
- 状态规范化
- 状态文件创建
- Obsidian 指定主题目录扫描
- Zotero 状态标签替换逻辑
- 所有 Python 脚本语法编译

结果：6/6 测试通过。

## 未在当前构建环境做真实联机测试

当前容器没有用户本机 Zotero/Better BibTeX/Obsidian，因此下列部分做了接口实现与静态检查，但需要用户在 Windows 11 本机首次初始化时验证：

- Zotero Local API 读取
- Better BibTeX JSON-RPC citekey 获取
- Zotero PDF 路径解析与复制
- Zotero 注释读取
- Zotero Local API 授权写 Tag

这些接口均依据 Zotero / Better BibTeX 官方文档设计，并且失败时应 fail-closed，不允许回退到直接写 SQLite。
