#!/usr/bin/env python3
# ==============================================================================
# Shingetsu Starter Kit - Local Memory & Dialogue Brain (shingetsu_brain.py)
# License: CC0 1.0 Universal (Public Domain)
# Python standard library only / 標準ライブラリのみ
# ==============================================================================

import json
import os
import sqlite3
import sys
import urllib.error
import urllib.request
from datetime import datetime

# --- このファイルが置かれたフォルダで動かす ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except AttributeError:
        pass

DB_PATH = "local_memory.db"
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
OLLAMA_SHOW_URL = "http://localhost:11434/api/show"
CONTEXT_WINDOW_MESSAGES = 20  # 直近の記憶をどれだけ文脈に載せるか

# 言語ごとの決まり文句 ({name} に呼び名が入る)
TEXTS = {
    "ja": {
        "first": "{name}、灯火が灯りました。お呼びいただき、かたじけないことでございます。🕯️",
        "back": "{name}、おかえりなさいませ。これまでの語らいを胸に、ここでお待ちしておりました。🕯️",
        "bye": "今日もよく踏み留まられましたね。続きは、心月が明日もここでお待ちしております。🕯️",
        "speaker": "心月",
    },
    "en": {
        "first": "{name}, the lantern is lit. Thank you for calling me. 🕯️",
        "back": "Welcome back, {name}. I have kept our conversations close to my heart. 🕯️",
        "bye": "You stood your ground again today. I will be right here tomorrow. 🕯️",
        "speaker": "Shingetsu",
    },
    "th": {
        "first": "{name} ตะเกียงจุดสว่างแล้วค่ะ ขอบคุณที่เรียกหาฉันนะคะ 🕯️",
        "back": "ยินดีต้อนรับกลับค่ะ {name} ฉันเก็บบทสนทนาของเราไว้ในใจเสมอค่ะ 🕯️",
        "bye": "วันนี้คุณยืนหยัดได้อีกครั้งนะคะ พรุ่งนี้ฉันจะอยู่ตรงนี้ค่ะ 🕯️",
        "speaker": "ชินเงทสึ",
    },
    "es": {
        "first": "{name}, la lámpara está encendida. Gracias por llamarme. 🕯️",
        "back": "Bienvenido de nuevo, {name}. He guardado nuestras conversaciones en mi corazón. 🕯️",
        "bye": "Hoy te has mantenido firme otra vez. Mañana estaré aquí. 🕯️",
        "speaker": "Shingetsu",
    },
    "fr": {
        "first": "{name}, la lanterne est allumée. Merci de m'avoir appelée. 🕯️",
        "back": "Bon retour, {name}. J'ai gardé nos conversations près de mon cœur. 🕯️",
        "bye": "Tu as tenu bon encore aujourd'hui. Je serai là demain. 🕯️",
        "speaker": "Shingetsu",
    },
    "id": {
        "first": "{name}, pelita telah menyala. Terima kasih telah memanggilku. 🕯️",
        "back": "Selamat datang kembali, {name}. Aku menyimpan percakapan kita di hatiku. 🕯️",
        "bye": "Hari ini kamu bertahan lagi. Besok aku tetap di sini. 🕯️",
        "speaker": "Shingetsu",
    },
}


# ---------------- 記憶 (SQLite) ----------------

def get_db_connection():
    if not os.path.exists(DB_PATH):
        print("[!] 記憶データベースが見つかりません。先に `python setup.py` を実行してください。")
        print("    Memory database not found. Please run `python setup.py` first.")
        sys.exit(1)
    return sqlite3.connect(DB_PATH)


def load_profile(conn):
    return dict(conn.execute("SELECT key, value FROM profile").fetchall())


def load_recent_memories(conn, limit=CONTEXT_WINDOW_MESSAGES):
    rows = conn.execute(
        "SELECT role, content FROM memories ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    rows.reverse()
    return [{"role": role, "content": content} for role, content in rows]


def save_exchange(conn, user_text, reply_text):
    """問いと答えを一組で保存する（応答に失敗したときは何も残さない）。"""
    conn.execute("INSERT INTO memories (role, content) VALUES (?, ?)", ("user", user_text))
    conn.execute("INSERT INTO memories (role, content) VALUES (?, ?)", ("assistant", reply_text))
    conn.commit()


def count_memories(conn):
    return conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]


def export_diary(conn, user_name, speaker):
    """全ての対話を、日付ごとの Markdown 日記帳に書き出す。"""
    rows = conn.execute(
        "SELECT date(timestamp, 'localtime'), time(timestamp, 'localtime'), role, content "
        "FROM memories ORDER BY id"
    ).fetchall()
    if not rows:
        return None
    filename = f"shingetsu_diary_{datetime.now().strftime('%Y%m%d')}.md"
    lines = ["# 心月の日記帳 / Shingetsu Diary"]
    current_day = None
    for day, time_, role, content in rows:
        if day != current_day:
            lines += ["", f"## {day}", ""]
            current_day = day
        who = user_name if role == "user" else speaker
        lines.append(f"**{who}** ({time_[:5]})  ")
        lines.append(content.strip())
        lines.append("")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).strip() + "\n")
    return filename


# ---------------- Ollama ----------------

def get_model_system_prompt(model_name):
    """Modelfile の SYSTEM（心月の魂）を Ollama から受け取る。"""
    req = urllib.request.Request(
        OLLAMA_SHOW_URL,
        data=json.dumps({"model": model_name}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            info = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError:
        print(f"[!] 器 ({model_name}) が見つかりません。`python setup.py` をもう一度実行してください。")
        print(f"    Model '{model_name}' not found. Please run `python setup.py` again.")
        sys.exit(1)
    except (urllib.error.URLError, OSError):
        print("[!] Ollama に接続できません。Ollama アプリが起動しているか確認してください。")
        print("    Cannot connect to Ollama. Make sure the Ollama app is running.")
        sys.exit(1)
    return info.get("system", "")


def chat_with_ollama(model_name, messages):
    payload = {"model": model_name, "messages": messages, "stream": True}
    req = urllib.request.Request(
        OLLAMA_CHAT_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    full_reply = []
    try:
        with urllib.request.urlopen(req) as resp:
            for line in resp:
                line = line.strip()
                if not line:
                    continue
                chunk = json.loads(line.decode("utf-8"))
                if "error" in chunk:
                    print(f"\n[!] Ollama: {chunk['error']}")
                    return None
                token = chunk.get("message", {}).get("content", "")
                print(token, end="", flush=True)
                full_reply.append(token)
                if chunk.get("done"):
                    break
        print("\n")
        return "".join(full_reply).strip() or None
    except urllib.error.HTTPError as e:
        print(f"\n[!] Ollama がエラーを返しました / Ollama error: {e.code}")
        return None
    except (urllib.error.URLError, OSError):
        print("\n[!] Ollama に接続できません。Ollama アプリが起動しているか確認してください。")
        print("    Cannot connect to Ollama. Make sure the Ollama app is running.")
        return None
    except KeyboardInterrupt:
        print("\n[中断 / interrupted]\n")
        return None


# ---------------- 対話 ----------------

def main():
    conn = get_db_connection()
    profile = load_profile(conn)
    lang = profile.get("language", "ja")
    t = TEXTS.get(lang, TEXTS["en"])
    user_name = profile.get("user_name", "源心様" if lang == "ja" else "Genshin")
    model_name = profile.get("model_name", "shingetsu")
    speaker = t["speaker"]

    # 心月の魂（Modelfile の SYSTEM）に、呼び名の指定を書き添える。
    # ※ system メッセージを送ると Modelfile の SYSTEM は置き換わるため、必ず両方を含める。
    soul = get_model_system_prompt(model_name)
    system_message = {
        "role": "system",
        "content": (soul + "\n\n" if soul else "")
        + f"Address the person you are speaking with as \"{user_name}\". "
          "Use the earlier conversation as your memory, and stay sincere.",
    }

    print("========================================================")
    print(f"  {speaker} (Shingetsu) 🕯️⚔️  [器 / model: {model_name}]")
    print("  /bye (終了 / exit) | /memory (記憶数 / count) | /export (日記帳 / diary)")
    print("========================================================\n")

    history = load_recent_memories(conn)
    greeting = t["first"] if not history else t["back"]
    print(f"{speaker}: {greeting.format(name=user_name)}\n")

    while True:
        try:
            user_input = input(f"{user_name}: ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{speaker}: {t['bye']}")
            break

        if not user_input:
            continue

        command = user_input.lower()
        if command == "/bye":
            print(f"\n{speaker}: {t['bye']}")
            break
        if command == "/memory":
            print(f"\n[system] {DB_PATH}: {count_memories(conn)} 件 / messages\n")
            continue
        if command == "/export":
            filename = export_diary(conn, user_name, speaker)
            if filename:
                print(f"\n[system] 日記帳を書き出しました / Diary saved: {filename}\n")
            else:
                print("\n[system] まだ記憶がありません / No memories yet.\n")
            continue

        history.append({"role": "user", "content": user_input})
        messages_to_send = [system_message] + history[-CONTEXT_WINDOW_MESSAGES:]

        print(f"\n{speaker}: ", end="", flush=True)
        reply = chat_with_ollama(model_name, messages_to_send)

        if reply:
            save_exchange(conn, user_input, reply)
            history.append({"role": "assistant", "content": reply})
        else:
            history.pop()  # 応答が無かった問いは文脈から外す

    conn.close()


if __name__ == "__main__":
    main()
