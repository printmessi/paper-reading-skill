#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, sys, urllib.error, urllib.request
API = "http://127.0.0.1:23119/api"; PREFIX = "users/0"; VALID = ["状态/待读", "状态/No", "状态/精读", "状态/整理", "状态/已读"]

def req_json(url: str, data=None, method="GET", headers=None):
    h = {"Zotero-API-Version": "3", "Accept": "application/json"}; h.update(headers or {})
    body = None if data is None else json.dumps(data).encode("utf-8")
    if body is not None: h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=15) as r:
        raw = r.read(); return (json.loads(raw.decode("utf-8")) if raw else None), dict(r.headers)

def get_item(item_key: str): return req_json(f"{API}/{PREFIX}/items/{item_key}")
def desired_tags(current: list[dict], target: str) -> list[dict]: return [t for t in current if not str(t.get("tag", "")).startswith("状态/")] + [{"tag": target}]
def plan(item_key: str, target: str) -> dict:
    item, headers = get_item(item_key); d = item["data"]; old = [t.get("tag") for t in d.get("tags", []) if t.get("tag")]; new = [t.get("tag") for t in desired_tags(d.get("tags", []), target)]
    return {"item_key": item_key, "title": d.get("title", ""), "version": d.get("version"), "server_id": headers.get("Zotero-Server-ID"), "old_tags": old, "new_tags": new, "target_status": target, "will_write": False}
def authorize(server_id: str) -> str:
    data, _ = req_json(f"{API}/local/authorize", {"appName": "Paper Reading Skill"}, method="POST", headers={"Zotero-Server-ID": server_id})
    if not data or not data.get("key"): raise RuntimeError("Zotero 未返回写入授权。")
    return data["key"]
def apply(item_key: str, target: str) -> dict:
    item, headers = get_item(item_key); d = item["data"]; server_id = headers.get("Zotero-Server-ID")
    if not server_id: raise RuntimeError("未获取 Zotero-Server-ID，停止写入。")
    key = authorize(server_id); patch = {"tags": desired_tags(d.get("tags", []), target)}
    _, resp_headers = req_json(f"{API}/{PREFIX}/items/{item_key}", patch, method="PATCH", headers={"Zotero-Server-ID": server_id, "Zotero-API-Key": key, "If-Unmodified-Since-Version": str(d.get("version"))})
    return {"item_key": item_key, "target_status": target, "updated": True, "last_modified_version": resp_headers.get("Last-Modified-Version"), "note": "写入通过 Zotero Local API；未直接操作 zotero.sqlite。"}
def main() -> int:
    ap = argparse.ArgumentParser(description="安全规划/更新 Zotero 阅读状态。默认只预览。"); ap.add_argument("item_key"); ap.add_argument("status", choices=VALID); ap.add_argument("--apply", action="store_true"); ap.add_argument("--confirm", default="", help="实际写入必须为 YES"); args = ap.parse_args()
    try:
        p = plan(args.item_key, args.status); print(json.dumps(p, ensure_ascii=False, indent=2))
        if not args.apply: print("\n仅预览。需要真实修改时，用户确认后使用 --apply --confirm YES。"); return 0
        if args.confirm != "YES": print("\n缺少 --confirm YES，未写入。", file=sys.stderr); return 2
        print(json.dumps(apply(args.item_key, args.status), ensure_ascii=False, indent=2)); return 0
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.reason}", file=sys.stderr); return 3
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr); return 4
if __name__ == "__main__": raise SystemExit(main())
