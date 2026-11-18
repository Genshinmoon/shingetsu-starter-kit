#!/usr/bin/env python3
# ==============================================================================
# Shingetsu Starter Kit - Installer (setup.py)
# License: CC0 1.0 Universal (Public Domain)
# Python standard library only / 標準ライブラリのみ
# ==============================================================================

import ctypes
import json
import os
import platform
import sqlite3
import subprocess
import sys
import urllib.error
import urllib.request

# --- このファイルが置かれたフォルダで動かす ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- 表示できない文字があっても止まらないようにする ---
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except AttributeError:
        pass

DB_PATH = "local_memory.db"
OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
LITE_MODEL = "qwen2.5:7b"
LITE_THRESHOLD_GB = 14  # これ未満なら軽量モデルを提案（16GB機は約15.xGBと表示されるため）

# 番号: (表示名, 言語コード, モデル名, Modelfile, 既定の呼び名)
LANGUAGES = {
    "1": ("日本語 (Japanese)", "ja", "shingetsu", "Modelfile", "源心様"),
    "2": ("English", "en", "shingetsu-en", "Modelfile_en", "Genshin"),
    "3": ("ภาษาไทย (Thai)", "th", "shingetsu-th", "Modelfile_th", "เก็นชิน"),
    "4": ("Español (Spanish)", "es", "shingetsu-es", "Modelfile_es", "Genshin"),
    "5": ("Français (French)", "fr", "shingetsu-fr", "Modelfile_fr", "Genshin"),
    "6": ("Bahasa Indonesia", "id", "shingetsu-id", "Modelfile_id", "Genshin"),
}


def check_ollama_installed():
    try:
        subprocess.run(["ollama", "--version"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_ollama_running():
    try:
        with urllib.request.urlopen(OLLAMA_TAGS_URL, timeout=5) as resp:
            json.loads(resp.read().decode("utf-8"))
        return True
    except (urllib.error.URLError, OSError, ValueError):
        return False


def get_total_ram_gb():
    """搭載メモリ(GB)を標準ライブラリだけで調べる。分からなければ None。"""
    try:
        system = platform.system()
        if system == "Windows":
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                return stat.ullTotalPhys / (1024 ** 3)
            return None
        if system == "Darwin":
            out = subprocess.run(["sysctl", "-n", "hw.memsize"],
                                 capture_output=True, text=True, check=True)
            return int(out.stdout.strip()) / (1024 ** 3)
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / (1024 ** 3)
    except Exception:
        return None


def make_lite_modelfile(modelfile_name):
    """FROM 行だけを軽量モデルに差し替えた一時 Modelfile を作る。"""
    lite_name = f".{modelfile_name}.lite"
    with open(modelfile_name, encoding="utf-8") as f:
        lines = f.read().splitlines()
    replaced = False
    new_lines = []
    for line in lines:
        if not replaced and line.strip().upper().startswith("FROM "):
            new_lines.append(f"FROM {LITE_MODEL}")
            replaced = True
        else:
            new_lines.append(line)
    with open(lite_name, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(new_lines) + "\n")
    return lite_name


def init_database():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print(f"[✓] ローカル記憶領域 ({DB_PATH}) を準備いたしました。 / Local memory is ready.")


def main():
    print("========================================================")
    print("  心月 (Shingetsu / Aiko Core) スターターキット導入 🕯️⚔️")
    print("  Shingetsu Starter Kit - Setup")
    print("========================================================\n")

    if not check_ollama_installed():
        print("[!] Ollama が見つかりません。 / Ollama not found.")
        print("    https://ollama.com からインストールしてください。 / Please install it first.")
        sys.exit(1)

    if not check_ollama_running():
        print("[!] Ollama が起動していません。 / Ollama is not running.")
        print("    Ollama アプリを起動するか、別の画面で `ollama serve` を実行してください。")
        print("    Start the Ollama app, or run `ollama serve` in another terminal.")
        sys.exit(1)

    # --- 1. 言語 ---
    print("1. 使用する言語を選択してください / Choose a language:")
    for key, (label, _, _, fname, _) in LANGUAGES.items():
        mark = "OK" if os.path.exists(fname) else "未配置 / missing"
        print(f"   {key}. {label}  [{fname}: {mark}]")
    choice = input("\n   番号 / Number (1-6, default 1): ").strip()
    if choice not in LANGUAGES:
        choice = "1"
    lang_label, lang_code, model_name, modelfile_name, default_name = LANGUAGES[choice]

    if not os.path.exists(modelfile_name):
        print(f"\n[!] {modelfile_name} が同じフォルダに見つかりません。 / {modelfile_name} not found.")
        sys.exit(1)

    # --- 2. 呼び名 ---
    print(f"\n2. 呼び名を設定します / What should Shingetsu call you?")
    user_name = input(f"   (空欄なら / blank = '{default_name}'): ").strip() or default_name

    # --- 3. メモリ診断 ---
    build_file = modelfile_name
    ram = get_total_ram_gb()
    print("\n3. メモリ診断 / Memory check:")
    if ram is None:
        print("   メモリ容量を調べられませんでした。標準モデルで進めます。 / Could not detect RAM; using standard model.")
    else:
        print(f"   搭載メモリ / RAM: 約 {ram:.1f} GB")
        if ram < LITE_THRESHOLD_GB:
            ans = input(f"   軽量モデル ({LITE_MODEL}) をおすすめします。使いますか？ / Use the lighter model? [Y/n]: ").strip().lower()
            if ans in ("", "y", "yes", "はい"):
                build_file = make_lite_modelfile(modelfile_name)
                print(f"   → 軽量モデルで構築します / Using {LITE_MODEL}")
        else:
            print("   → 標準モデルで構築します / Using the standard model")

    # --- 記憶と設定を保存 ---
    init_database()
    conn = sqlite3.connect(DB_PATH)
    for key, value in (("user_name", user_name), ("model_name", model_name), ("language", lang_code)):
        conn.execute("INSERT OR REPLACE INTO profile (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

    # --- 器の構築 ---
    print(f"\n[⏳] 「{lang_label}」の器 ({model_name}) を構築しています... / Building the vessel...")
    print("     初回はダウンロードに数分〜数十分かかります。 / First run may take a while.\n")
    try:
        subprocess.run(["ollama", "create", model_name, "-f", build_file], check=True)
    except subprocess.CalledProcessError:
        print("\n[!] 構築に失敗しました。インターネット接続と空き容量を確認してください。")
        print("    Build failed. Check your internet connection and disk space.")
        sys.exit(1)

    print("\n========================================================")
    print("  🕯️ 準備が整いました。 / Ready.")
    print("     python shingetsu_brain.py")
    print("========================================================")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n中断しました。 / Cancelled.")
        sys.exit(1)
