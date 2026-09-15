#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "http://127.0.0.1:23119/api"
BBT = "http://127.0.0.1:23119/better-bibtex/json-rpc"
PREFIX = "users/0"


def request_json(url: str):
    req = urllib.request.Request(url, headers={"Zotero-API-Version": "3", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        raw = r.read().decode("utf-8").strip()
        return (json.loads(raw) if raw else {}), dict(r.headers)


def request_probe(url: str):
    req = urllib.request.Request(url, headers={"Zotero-API-Version": "3", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        raw = r.read().decode("utf-8", errors="replace").strip()
        try:
            body = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            body = {"raw_preview": raw[:200]}
        return body, dict(r.headers)


def request_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"Zotero-API-Version": "3", "Accept": "text/plain"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.read().decode("utf-8").strip()


def bbt_rpc(method: str, params: list):
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode("utf-8")
    req = urllib.request.Request(
        BBT,
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode("utf-8"))
    if "error" in data:
        raise RuntimeError(data["error"])
    return data.get("result")


def print_json(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def api_url(path: str) -> str:
    return f"{API.rstrip('/')}/{path.lstrip('/')}"


def search_items(query: str, limit: int = 10):
    q = urllib.parse.urlencode({"q": query, "limit": limit, "format": "json"})
    data, _ = request_json(api_url(f"{PREFIX}/items/top?{q}"))
    return data


def get_item(key: str):
    data, headers = request_json(api_url(f"{PREFIX}/items/{key}"))
    return data, headers


def get_children(key: str):
    data, _ = request_json(api_url(f"{PREFIX}/items/{key}/children?format=json"))
    return data


def extract_creators(data: dict) -> list[str]:
    out = []
    for c in data.get("creators", []):
        name = c.get("name") or " ".join(x for x in [c.get("firstName", ""), c.get("lastName", "")] if x).strip()
        if name:
            out.append(name)
    return out


def summarize_item(obj: dict) -> dict:
    data = obj.get("data", obj)
    return {
        "key": data.get("key", obj.get("key", "")),
        "title": data.get("title", ""),
        "itemType": data.get("itemType", ""),
        "date": data.get("date", ""),
        "DOI": data.get("DOI", ""),
        "creators": extract_creators(data),
        "tags": [t.get("tag") for t in data.get("tags", []) if t.get("tag")],
        "collections": data.get("collections", []),
        "version": data.get("version", obj.get("version")),
    }


def find_pdf_attachment(item_key: str):
    children = get_children(item_key)
    pdfs = []
    for child in children:
        d = child.get("data", child)
        ctype = (d.get("contentType") or "").lower()
        filename = d.get("filename", "")
        if ctype == "application/pdf" or filename.lower().endswith(".pdf"):
            pdfs.append(d)
    return pdfs


def file_url_for_attachment(attachment_key: str) -> str:
    return request_text(api_url(f"{PREFIX}/items/{attachment_key}/file/view/url"))


def file_url_to_path(url: str) -> Path:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "file":
        raise ValueError(f"不是 file:// URL：{url}")
    path = urllib.request.url2pathname(parsed.path)
    if sys.platform.startswith("win") and path.startswith("/") and len(path) > 3 and path[2] == ":":
        path = path[1:]
    return Path(path)


def copy_pdf(item_key: str, dest_dir: Path) -> dict:
    pdfs = find_pdf_attachment(item_key)
    if not pdfs:
        raise RuntimeError("该 Zotero 条目未找到 PDF 附件。请先把主论文 PDF 加入 Zotero。")
    attachment = pdfs[0]
    url = file_url_for_attachment(attachment["key"])
    src = file_url_to_path(url)
    if not src.exists():
        raise FileNotFoundError(src)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.copy2(src, dest)
    return {"source": str(src), "copied_to": str(dest), "attachment_key": attachment["key"], "pdf_count": len(pdfs), "note": "Zotero 原 PDF 未修改；分析应针对工作区副本。"}


def get_annotations(item_key: str) -> list[dict]:
    results = []
    for att in find_pdf_attachment(item_key):
        for child in get_children(att["key"]):
            d = child.get("data", child)
            if d.get("itemType") != "annotation":
                continue
            results.append({"attachment_key": att["key"], "annotation_key": d.get("key"), "annotationType": d.get("annotationType"), "text": d.get("annotationText", ""), "comment": d.get("annotationComment", ""), "pageLabel": d.get("annotationPageLabel", ""), "color": d.get("annotationColor", "")})
    return results


def classify_annotation(a: dict) -> str:
    comment = (a.get("comment") or "").strip()
    text = (a.get("text") or "").strip()
    lower = comment.lower()
    if any(k in lower for k in ["?", "没看懂", "不懂", "问题", "todo", "why"]): return "待解决问题"
    if any(k in lower for k in ["灵感", "想法", "idea", "可以做", "联想"]): return "灵感/联想"
    if comment: return "个人批注"
    if text: return "高亮摘录"
    return "其他"


def main() -> int:
    ap = argparse.ArgumentParser(description="Zotero Local API/Better BibTeX 只读辅助工具。绝不直接读写 zotero.sqlite。")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    p = sub.add_parser("search"); p.add_argument("query"); p.add_argument("--limit", type=int, default=10)
    p = sub.add_parser("item"); p.add_argument("item_key")
    p = sub.add_parser("citekey"); p.add_argument("item_key")
    p = sub.add_parser("copy-pdf"); p.add_argument("item_key"); p.add_argument("--dest", required=True)
    p = sub.add_parser("annotations"); p.add_argument("item_key")
    args = ap.parse_args()
    try:
        if args.cmd == "check":
            data, headers = request_probe(api_url(""))
            try: bbt = bbt_rpc("api.ready", [])
            except Exception as e: bbt = {"available": False, "error": str(e)}
            print_json({"zotero_local_api": {"available": True, "server_id": headers.get("Zotero-Server-ID"), "data": data}, "better_bibtex": bbt}); return 0
        if args.cmd == "search": print_json([summarize_item(x) for x in search_items(args.query, args.limit)]); return 0
        if args.cmd == "item":
            item, _ = get_item(args.item_key); summary = summarize_item(item); summary["pdf_attachments"] = [{"key": p.get("key"), "filename": p.get("filename"), "contentType": p.get("contentType")} for p in find_pdf_attachment(args.item_key)]; print_json(summary); return 0
        if args.cmd == "citekey":
            result = bbt_rpc("item.citationkey", [[args.item_key]]); print_json({"item_key": args.item_key, "citekey": (result or {}).get(args.item_key)}); return 0
        if args.cmd == "copy-pdf": print_json(copy_pdf(args.item_key, Path(args.dest).expanduser().resolve())); return 0
        if args.cmd == "annotations":
            anns = get_annotations(args.item_key)
            for a in anns: a["category"] = classify_annotation(a)
            print_json(anns); return 0
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.reason}", file=sys.stderr)
        if e.code == 403: print("提示：请在 Zotero Settings → Advanced 中允许本机应用通信。", file=sys.stderr)
        return 3
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr); return 4
    return 0

if __name__ == "__main__": raise SystemExit(main())
