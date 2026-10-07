#!/usr/bin/env python3
"""Rachel 静帧闸门。

未写入 reviews/<id>/APPROVED 时，拒绝整段 MP4。
静帧只调用花叔 render.py 的 --stills。
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "vendor" / "huashu-art-motion" / "scripts" / "engine" / "render.py"
REVIEWS = ROOT / "reviews"
ASSETS = ROOT / "assets"

FORMAT_BLOCK = """格式：PNG，真正的透明通道。背景全透明。不要棋盘格，不要白底、灰底、渐变、地板、接触影子、画框、水印、文字。主体放在画布正中，四周留空。如果做不出透明通道，不要画棋盘格，改用纯色 #00FF00 绿底，画面里不许再有任何绿色，并在回复里写明「这是绿底，不是透明」。"""

MOTIONS = {"kinetic-type", "shape-morph", "spring", "beat-hold", "pull-back"}
STYLES = {
    "23_dali": "达利",
    "17_ink": "水墨",
    "12_bauhaus": "包豪斯",
    "19_munch": "蒙克",
    "22_constructivism": "构成主义",
    "16_2026": "当代扁平",
    "09_postimp": "梵高",
}


def python_with_playwright() -> str | None:
    candidates = [os.environ.get("RACHEL_PYTHON"), sys.executable]
    home = Path.home()
    candidates.extend(str(path) for path in home.glob(".local/share/*/.venv/bin/python"))
    candidates.extend(str(path) for path in home.glob(".local/share/*/*/.venv/bin/python"))
    seen = set()
    for cand in candidates:
        if not cand or cand in seen or not Path(cand).exists():
            continue
        seen.add(cand)
        probe = subprocess.run([cand, "-c", "import playwright"], capture_output=True)
        if probe.returncode == 0:
            return cand
    return None


def launch(engine_args: list[str]) -> list[str]:
    py = python_with_playwright()
    if py:
        return [py, str(ENGINE), *engine_args]
    if not shutil.which("uv"):
        raise SystemExit("没有带 Playwright 的 Python，也没有 uv")
    return ["uv", "run", "--with", "playwright", "python", str(ENGINE), *engine_args]


def load_board(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data.get("id") or not isinstance(data.get("beats"), list) or not data["beats"]:
        raise SystemExit("分镜缺少 id 或 beats")
    for beat in data["beats"]:
        for key in ("id", "start_s", "end_s", "subtitle", "action", "style_id", "motion"):
            if key not in beat:
                raise SystemExit(f"镜 {beat.get('id')} 缺少 {key}")
        if beat["motion"] not in MOTIONS:
            raise SystemExit(f"镜 {beat['id']} 的动效 {beat['motion']} 不在允许列表里")
        if beat.get("reversal") and beat["motion"] != "pull-back":
            raise SystemExit(f"反转镜 {beat['id']} 的动效必须是 pull-back")
        if beat["end_s"] <= beat["start_s"]:
            raise SystemExit(f"镜 {beat['id']} 的时间倒了")
    return data


def png_has_alpha(path: Path) -> bool:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or len(data) < 26:
        return False
    # IHDR 颜色类型：4 灰阶+alpha，6 真彩+alpha。
    color_type = data[25]
    if color_type in (4, 6):
        return True
    return b"tRNS" in data


def asset_list(board: dict) -> list[dict]:
    raw = board.get("assets") or []
    if not isinstance(raw, list):
        raise SystemExit("assets 必须是数组。这一支没有要生的图就写 []")
    for item in raw:
        for key in ("file", "subject"):
            if not item.get(key):
                raise SystemExit(f"素材缺少 {key}")
        if not str(item["file"]).endswith(".png"):
            raise SystemExit(f"{item['file']} 必须是 .png")
    return raw


def asset_dir(board: dict) -> Path:
    return ASSETS / board["id"]


def asset_problems(board: dict) -> list[str]:
    found = []
    for item in asset_list(board):
        path = asset_dir(board) / item["file"]
        if not path.exists():
            found.append(f"缺少 {path}")
            continue
        if not png_has_alpha(path):
            found.append(f"{item['file']} 不是带透明通道的 PNG。绿底图要先抠掉再交。")
    return found


def review_dir(board: dict) -> Path:
    return REVIEWS / board["id"]


def approved(board: dict) -> bool:
    text = (review_dir(board) / "APPROVED").read_text(encoding="utf-8") if (review_dir(board) / "APPROVED").exists() else ""
    return "通过" in text


def still_times(beat: dict) -> list[float]:
    times = [round(float(beat["start_s"]) + 0.35, 2)]
    if beat.get("reversal"):
        times.append(round(float(beat["end_s"]) - 0.35, 2))
    return times


def problems(board: dict) -> list[str]:
    found = []
    duration = float(board.get("duration_s") or 0)
    if board.get("source") != "fixture" and not 88 <= duration <= 90:
        found.append(f"时长 {duration} 秒，不在 88–90 秒")
    if board.get("source") == "life-guide" and not board.get("life_guide"):
        found.append("来源是人生指南，但没有第几节第几条")
    reversal = [b for b in board["beats"] if b.get("reversal")]
    if len(reversal) != 1:
        found.append(f"反转镜应有且只有 1 个，现在是 {len(reversal)} 个")
    for beat in board["beats"]:
        if beat["style_id"] not in STYLES:
            found.append(f"镜 {beat['id']} 的画风 {beat['style_id']} 没有对应场景，不能新写渲染器")
    return found


def write_packet(board: dict) -> Path:
    dest = review_dir(board)
    dest.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# 审查包 {board['title']}",
        "",
        f"- id：{board['id']}",
        f"- 来源：{board.get('source', '')}",
        f"- 洞察：{board.get('insight', '')}",
        "",
        "## 闸门还没过的原因",
        "",
    ]
    issues = problems(board)
    if issues:
        lines.extend(f"- {item}" for item in issues)
    else:
        lines.append("- 分镜表本身没有结构性问题。下面每一镜仍要看图。")
    lines.extend(["", "## 接触表", ""])
    for beat in board["beats"]:
        style = STYLES.get(beat["style_id"], "缺失")
        lines.append(
            f"- {beat['id']} {beat['start_s']}–{beat['end_s']}s"
            f" [{style} / {beat['motion']}] {beat['subtitle']}"
        )
        lines.append(f"  动作：{beat['action']}")
        for t in still_times(beat):
            lines.append(f"  静帧：stills/{beat['id']}-t{t:06.2f}.png")
        lines.append("  审查：画风 / 素材边缘 / 字幕 / 动效 / 反转 / 没有鸡汤，每项是或否")
    lines.extend(
        [
            "",
            "## 清单",
            "",
            "逐项见 references/keyframe-review.md。有一项为否就整包打回。",
            "",
            "用户回复「通过」之后，把这个词写入：",
            "",
            f"`{dest / 'APPROVED'}`",
            "",
        ]
    )
    path = dest / "审查包.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def still_commands(board: dict, out: Path) -> list[list[str]]:
    commands = []
    for beat in board["beats"]:
        # --solo 的时间是这一段内部的局部时间，用 0.35 看风格是否活着。
        # 反转第二张用较晚的局部时间，避免和第一张是同一帧。
        local = ["0.35"]
        if beat.get("reversal"):
            local.append("1.10")
        commands.append(
            launch(
                [
                    "--film",
                    "gallery",
                    "--solo",
                    beat["style_id"],
                    "--stills",
                    ",".join(local),
                    "--no-counter",
                    "--out",
                    str(out / beat["id"]),
                ]
            )
        )
    return commands


def cmd_packet(board: dict) -> None:
    path = write_packet(board)
    print(path)


def cmd_prompts(board: dict) -> None:
    items = asset_list(board)
    dest = review_dir(board)
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "生图提示词.md"
    if not items:
        path.write_text(
            f"# {board['title']}\n\n这一支没有需要生图的素材。背景、字和几何用代码，直接出静帧。\n",
            encoding="utf-8",
        )
        print(path)
        return
    lines = [
        f"# {board['title']} 生图",
        "",
        f"一次贴一条到 ChatGPT。生成后按文件名存到 `assets/{board['id']}/`，再发回。",
        "同一主体的后面几张，要把第一张作为参考图一起上传。",
        "",
    ]
    for index, item in enumerate(items, start=1):
        canvas = item.get("canvas") or "1024×1024"
        lines.append(f"## {index}. {item['file']}")
        lines.append("")
        lines.append(item["subject"].strip())
        lines.append("")
        lines.append(f"画布 {canvas}。")
        lines.append(FORMAT_BLOCK)
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    print(path)


def cmd_assets(board: dict) -> None:
    items = asset_list(board)
    if not items:
        print("这一支没有要生的图，可以进入静帧。")
        return
    found = asset_problems(board)
    if found:
        raise SystemExit("素材还不能进视频。\n" + "\n".join(found))
    print(f"{len(items)} 张图都在，并且带透明通道。可以进入静帧。")


def cmd_stills(board: dict, execute: bool) -> None:
    if execute:
        found = asset_problems(board)
        if found:
            raise SystemExit("素材还没交齐，不出静帧。\n" + "\n".join(found))
    out = review_dir(board) / "stills"
    out.mkdir(parents=True, exist_ok=True)
    commands = still_commands(board, out)
    script = out / "commands.sh"
    script.write_text(
        "\n".join(" ".join(part) for part in commands) + "\n",
        encoding="utf-8",
    )
    if not execute:
        print("未执行渲染。命令写在", script)
        return
    if not ENGINE.exists():
        raise SystemExit(f"找不到花叔渲染器：{ENGINE}")
    for command in commands:
        print("运行", " ".join(command))
        subprocess.run(command, check=True, cwd=ENGINE.parent)


def cmd_render(board: dict, execute: bool) -> None:
    found = asset_problems(board)
    if found:
        raise SystemExit("素材还没交齐，不出视频。\n" + "\n".join(found))
    if problems(board):
        raise SystemExit("分镜还有结构性问题，先看审查包。\n" + "\n".join(problems(board)))
    if not approved(board):
        raise SystemExit(
            f"没有 {review_dir(board) / 'APPROVED'}，拒绝渲染 MP4。先出静帧并等用户回复「通过」。"
        )
    film = board.get("film")
    if not film:
        raise SystemExit("分镜还没有可渲染的 film（eras 文件）。静帧可以通过，整段 MP4 仍不渲染。")
    if not execute:
        print("已通过审查。加上 --execute 才会调用不带 --stills 的渲染。")
        return
    if not ENGINE.exists():
        raise SystemExit(f"找不到花叔渲染器：{ENGINE}")
    out = review_dir(board) / f"{board['id']}.mp4"
    command = launch(["--film", film, "--out", str(out)])
    print("运行", " ".join(command))
    subprocess.run(command, check=True, cwd=ENGINE.parent)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("packet", "stills", "render", "prompts", "assets"))
    parser.add_argument("--storyboard", type=Path)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if args.storyboard is None:
        raise SystemExit("这个命令需要 --storyboard")
    board = load_board(args.storyboard)
    if args.mode == "prompts":
        cmd_prompts(board)
    elif args.mode == "assets":
        cmd_assets(board)
    elif args.mode == "packet":
        cmd_packet(board)
    elif args.mode == "stills":
        cmd_stills(board, args.execute)
    else:
        cmd_render(board, args.execute)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
