#!/usr/bin/env python3
"""Generate images via TopView AI Text-to-Image API.

Usage:
    # Single image
    python3 topview_image_gen.py --prompt "..." --output path/to/output.png

    # Batch from JSON shot list
    python3 topview_image_gen.py --batch shot-list.json --output-dir path/to/dir/

Environment variables:
    TOPVIEW_API_KEY  — Bearer token for Authorization header
    TOPVIEW_UID      — User ID for Topview-Uid header
"""

import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = "https://api.topview.ai"
MODEL = "GPT Image 2"
ASPECT_RATIO = "16:9"
RESOLUTION = "2K"
POLL_INTERVAL = 3
POLL_TIMEOUT = 300

def _ssl_ctx():
    ctx = ssl.create_default_context()
    try:
        ctx.load_default_certs()
    except Exception:
        pass
    if os.environ.get("TOPVIEW_NO_VERIFY_SSL"):
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _check_credentials():
    api_key = os.environ.get("TOPVIEW_API_KEY")
    uid = os.environ.get("TOPVIEW_UID")
    if not api_key or not uid:
        print("Error: TOPVIEW_API_KEY and TOPVIEW_UID environment variables are required.", file=sys.stderr)
        print("  export TOPVIEW_API_KEY='your-api-key'", file=sys.stderr)
        print("  export TOPVIEW_UID='your-user-id'", file=sys.stderr)
        sys.exit(1)


def _headers():
    return {
        "Authorization": f"Bearer {os.environ['TOPVIEW_API_KEY']}",
        "Topview-Uid": os.environ["TOPVIEW_UID"],
        "Content-Type": "application/json",
    }


def _post(path: str, body: dict) -> dict:
    data = json.dumps(body).encode()
    req = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers=_headers(), method="POST")
    with urllib.request.urlopen(req, timeout=30, context=_ssl_ctx()) as resp:
        return json.loads(resp.read())


def _get(path: str, params: dict) -> dict:
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{BASE_URL}{path}?{qs}"
    req = urllib.request.Request(url, headers=_headers(), method="GET")
    with urllib.request.urlopen(req, timeout=30, context=_ssl_ctx()) as resp:
        return json.loads(resp.read())


def submit_task(prompt: str) -> str:
    resp = _post("/v1/common_task/text2image/task/submit", {
        "model": MODEL,
        "prompt": prompt,
        "aspectRatio": ASPECT_RATIO,
        "resolution": RESOLUTION,
        "generateCount": 1,
    })
    if resp.get("code") != "200":
        raise RuntimeError(f"Submit failed: {resp.get('message')}")
    return resp["result"]["taskId"]


def poll_result(task_id: str) -> dict:
    deadline = time.time() + POLL_TIMEOUT
    while time.time() < deadline:
        resp = _get("/v1/common_task/text2image/task/query", {"taskId": task_id})
        if resp.get("code") != "200":
            raise RuntimeError(f"Query failed: {resp.get('message')}")
        result = resp["result"]
        status = result["status"]
        if status == "success":
            return result
        if status == "fail":
            raise RuntimeError(f"Task failed: {result.get('errorMsg')}")
        time.sleep(POLL_INTERVAL)
    raise TimeoutError(f"Task {task_id} timed out after {POLL_TIMEOUT}s")


def download_image(url: str, output: Path):
    output.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60, context=_ssl_ctx()) as resp:
        output.write_bytes(resp.read())


def generate_one(prompt: str, output: Path) -> bool:
    try:
        print(f"  Submitting: {output.name}")
        task_id = submit_task(prompt)
        print(f"  Polling task {task_id}...")
        result = poll_result(task_id)
        images = result.get("images", [])
        if not images or images[0]["status"].lower() != "success":
            err = images[0]["errorMsg"] if images else "No images returned"
            print(f"  ✗ {output.name}: {err}", file=sys.stderr)
            return False
        download_image(images[0]["filePath"], output)
        cost = result.get("costCredit", "?")
        print(f"  ✓ {output} ({images[0]['width']}x{images[0]['height']}, {cost} credits)")
        return True
    except (RuntimeError, TimeoutError, urllib.error.URLError) as e:
        print(f"  ✗ {output.name}: {e}", file=sys.stderr)
        return False


def run_single(prompt: str, output: str):
    ok = generate_one(prompt, Path(output))
    sys.exit(0 if ok else 1)


def run_batch(batch_file: str, output_dir: str):
    with open(batch_file, "r", encoding="utf-8") as f:
        items = json.load(f)
    out = Path(output_dir)
    total = len(items)
    ok_count = 0
    for i, item in enumerate(items, 1):
        print(f"\n[{i}/{total}]")
        if generate_one(item["prompt"], out / item["filename"]):
            ok_count += 1
    print(f"\nDone: {ok_count}/{total} succeeded")
    sys.exit(0 if ok_count == total else 1)


def main():
    parser = argparse.ArgumentParser(description="Generate images via TopView AI API")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompt", help="Single image prompt")
    group.add_argument("--batch", help="JSON file with prompt list")
    parser.add_argument("--output", help="Output path for single image")
    parser.add_argument("--output-dir", help="Output directory for batch mode")
    args = parser.parse_args()

    _check_credentials()

    if args.prompt:
        if not args.output:
            parser.error("--output is required with --prompt")
        run_single(args.prompt, args.output)
    else:
        if not args.output_dir:
            parser.error("--output-dir is required with --batch")
        run_batch(args.batch, args.output_dir)


if __name__ == "__main__":
    main()
