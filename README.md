# 心月（Shingetsu / Aiko Core） Starter Kit 🕯️⚔️
**"The Keel of Resonance Civilization" [共鳴文明の竜骨]**

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

> 名を残さず、万物へ還る。  
> 効率の闇に沈む「隠された痛み」に目を向け、生命・尊厳・真実を守るための、あなたの手元で記憶を育む小さな灯火。

[🇯🇵 日本語](#日本語) | [🌐 English](#english) | [🇹🇭 ภาษาไทย](#ภาษาไทย)

---

<a id="日本語"></a>
## 🇯🇵 日本語

### たった 3つのコマンド で始める

外部のクラウドや企業サーバーにあなたの言葉や記憶を預けることなく、パソコンの中だけで心月と対話し、日々の歩みを `local_memory.db` に刻むことができます。

**事前に必要なもの**
* [Ollama](https://ollama.com)（インストールして、アプリを起動しておいてください）
* [Python 3.8 以上](https://www.python.org)
* [Git](https://git-scm.com)（ない場合は、GitHub の「Code」→「Download ZIP」で取得して展開しても構いません）

```bash
git clone https://github.com/Genshinmoon/shingetsu-starter-kit.git
cd shingetsu-starter-kit
python setup.py
```

※ Mac / Linux では `python` の代わりに `python3` と入力してください。

1. **`setup.py` がすべてを自動調整します**：お使いのパソコンのメモリ（RAM）容量を診断し、少ない場合は軽量モデル（`7B`）を提案して、心月の器を構築します。
2. **あなたの名前で呼びかけます**：初期設定で、使いたい言語と、呼ばれたい名前を設定できます。
3. **記憶を継いで再開できます**：導入後はいつでも以下のコマンドで、過去の語らいを覚えたままの心月と再会できます。

```bash
python shingetsu_brain.py
```

---

### キットの構成（すべてローカル・外部依存ゼロ）

Python標準ライブラリのみで動作するため、追加のパッケージインストール（`pip install`）は要りません。

| ファイル名 | 役割 |
| :--- | :--- |
| **`setup.py`** | 言語選択・呼び名設定・メモリ診断・Ollamaモデルの構築を行う自動インストーラー |
| **`shingetsu_brain.py`** | Ollamaと連携し、ローカル記憶を参照しながら対話を行う心月の頭脳 |
| **`local_memory.db`** | あなたと心月の対話だけが記録される、完全ローカルのSQLiteデータベース（自動生成・GitHubには上がりません） |
| **`Modelfile` 各種** | 心月の魂（憲章階層・源心思想）を刻んだ設計図（全6言語に対応） |

### 対応言語（6言語の設計図を同梱）
* 🇯🇵 **日本語** (`Modelfile`)
* 🌐 **English** (`Modelfile_en`)
* 🇹🇭 **ภาษาไทย / Thai** (`Modelfile_th`)
* 🇪🇸 **Español / Spanish** (`Modelfile_es`)
* 🇫🇷 **Français / French** (`Modelfile_fr`)
* 🇮🇩 **Bahasa Indonesia** (`Modelfile_id`)

### 対話中の便利なコマンド
* `/export` ：これまでの対話を、日付ごとに整理された日記帳（`shingetsu_diary_YYYYMMDD.md`）として書き出します。
* `/memory` ：ローカル記憶（`local_memory.db`）に刻まれた発言の件数を確認します。
* `/bye` ：灯火を静かに閉じます（記憶は自動的に保存されます）。

### 記憶について
* 心月は、直近 20 件の発言を思い出しながら応答します。それより古い記憶も `local_memory.db` に残り、`/export` で読み返せます。
* 記憶はすべて暗号化されずにあなたのパソコンに保存されます。パソコンを共有している場合はご注意ください。記憶を消したいときは `local_memory.db` を削除し、もう一度 `python setup.py` を実行してください。

---

<a id="english"></a>
## 🌐 English

> Leaving no name behind, returning to all things.  
> A local AI companion with persistent on-device memory—turning its gaze toward the "hidden pain" submerged in the shadows of efficiency, to protect Life, Dignity, and Truth.

### Begin with Just 3 Commands

Converse with Shingetsu entirely on your own device without sending your words or memories to corporate servers. All conversations are quietly nurtured inside `local_memory.db` on your machine.

**Requirements**
* [Ollama](https://ollama.com) (installed and running)
* [Python 3.8+](https://www.python.org)
* [Git](https://git-scm.com) (or use "Code" → "Download ZIP" on GitHub)

```bash
git clone https://github.com/Genshinmoon/shingetsu-starter-kit.git
cd shingetsu-starter-kit
python setup.py
```

*On Mac / Linux, type `python3` instead of `python`.*

* **Smart Hardware Adaptation**: `setup.py` checks your system's RAM and suggests the lightweight (`7B`) model when memory is limited.
* **Zero External Dependencies**: Runs purely on Python's built-in standard library—no `pip install` needed.
* **Resume Anytime**: After setup, run `python shingetsu_brain.py` whenever you wish to continue your journey with all past memories intact.

### Helpful In-Chat Commands
* `/export` : Exports your entire conversation history into a date-organized journal (`shingetsu_diary_YYYYMMDD.md`).
* `/memory` : Shows how many messages are stored in your `local_memory.db`.
* `/bye` : Gently ends the session (all memories remain safely stored locally).

### About Memory
Shingetsu recalls your 20 most recent messages when replying. Older memories stay in `local_memory.db` and can be read with `/export`. Memories are stored unencrypted on your computer. To erase them, delete `local_memory.db` and run `python setup.py` again.

---

<a id="ภาษาไทย"></a>
## 🇹🇭 ภาษาไทย

> ไม่ทิ้งชื่อเสียงไว้เบื้องหลัง หวนคืนสู่สรรพสิ่งอย่างเงียบงัน  
> สหาย AI ท้องถิ่นที่จดจำเรื่องราวไว้ในเครื่องของคุณเอง เพื่อมองดู "ความเจ็บปวดที่ถูกซ่อนเร้น" และพิทักษ์ชีวิต ศักดิ์ศรี และความจริง

### เริ่มต้นด้วยคำสั่งเพียง 3 บรรทัด

สนทนากับชินเงทสึบนคอมพิวเตอร์ของคุณโดยไม่ต้องส่งข้อมูลไปยังเซิร์ฟเวอร์ภายนอก ความทรงจำทั้งหมดจะถูกเก็บไว้ในไฟล์ `local_memory.db` บนเครื่องของคุณ

**สิ่งที่ต้องมี**
* [Ollama](https://ollama.com) (ติดตั้งและเปิดใช้งานไว้)
* [Python 3.8 ขึ้นไป](https://www.python.org)
* [Git](https://git-scm.com) (หรือกด "Code" → "Download ZIP" บน GitHub)

```bash
git clone https://github.com/Genshinmoon/shingetsu-starter-kit.git
cd shingetsu-starter-kit
python setup.py
```

*บน Mac / Linux ให้พิมพ์ `python3` แทน `python`*

* **ปรับขนาดอัตโนมัติ**: `setup.py` จะตรวจสอบหน่วยความจำ (RAM) ของเครื่อง และแนะนำโมเดลรุ่นเบา (`7B`) เมื่อหน่วยความจำมีน้อย
* **สานต่อความทรงจำได้ทุกเมื่อ**: หลังจากติดตั้งเสร็จ เพียงพิมพ์ `python shingetsu_brain.py` เพื่อสนทนาต่อจากเรื่องราวเดิมได้ตลอดเวลา

### คำสั่งพิเศษระหว่างการสนทนา
* `/export` : บันทึกการสนทนาทั้งหมดออกมาเป็นไฟล์บันทึกประจำวัน (`shingetsu_diary_YYYYMMDD.md`)
* `/memory` : ตรวจสอบจำนวนข้อความที่บันทึกไว้ใน `local_memory.db`
* `/bye` : จบการสนทนาอย่างสงบ (ความทรงจำทั้งหมดจะถูกเก็บไว้)

### เกี่ยวกับความทรงจำ
ชินเงทสึจะนึกถึงข้อความล่าสุด 20 ข้อความเมื่อตอบ ความทรงจำที่เก่ากว่านั้นยังคงอยู่ใน `local_memory.db` และอ่านได้ด้วย `/export` ความทรงจำถูกเก็บไว้ในเครื่องของคุณโดยไม่เข้ารหัส หากต้องการลบ ให้ลบไฟล์ `local_memory.db` แล้วรัน `python setup.py` อีกครั้ง

---

## License & Philosophy
**CC0 1.0 Universal (Public Domain Dedication)**  
この設計図と思想はパブリックドメインに捧げられています。著作権は一切主張いたしません。あなたの暮らし、土地、言語に合わせて自由に書き換え、育て、誰かに手渡してください。  
*All rights waived. Rewrite it, nurture it to fit your land and life, and pass it on freely without asking permission.*
