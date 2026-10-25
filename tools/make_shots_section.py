"""從 screenshots/app_log.json 產生 notebook §8（Gradio 對話結果截圖）的 markdown。"""
import json, re
RAW = "https://raw.githubusercontent.com/arvin611ch/taica-lab06-turtle-soup/main/screenshots/"
log = json.load(open("screenshots/app_log.json", encoding="utf-8"))

intro = next(e for e in log if e.get("event") == "new_game")["intro"]
title = re.search(r"《(.+?)》", intro).group(1)
qa = [e for e in log if "q" in e]
hint = next(e for e in log if e.get("event") == "hint")["a"]
ai_intro = next(e for e in log if e.get("event") == "new_game_ai")["intro"]
ai_title = re.search(r"《(.+?)》", ai_intro).group(1)
ai_source = "AI 現煮" if "AI 現煮" in ai_intro else "店內菜單（AI 出題失敗自動退回）"
reveal = next(e for e in log if e.get("event") == "reveal")["a"]

def qa_block(items):
    return "  \n".join(f"> **客人：** {e['q']}  \n> **老湯：** {e['a'].splitlines()[0]}" for e in items)

first3, rest = qa[:3], qa[3:-1]   # 最後一題是 AI 現煮那局問的

md = f"""
## 8. Gradio 對話結果（實際操作截圖）

截圖是在本機跑 `app.py`（和 notebook 同一份程式，模型 `ollama:qwen2.5:14b`）、用 Playwright 真的點按鈕、打字送出後擷取的；每一張對應的對話全文在 repo 的 `screenshots/app_log.json`。流程：點一碗湯 → 問三題 → 按提示 → 再問到破案 → 換 AI 現煮 → 公布湯底。

**(1) 開店畫面。** 上方選難度、湯從哪來、主題；聊天區是老湯的開場白；下方是問題輸入框與三個功能鍵，最下面是計分板。

![start]({RAW}app_1_start.png)

**(2) 點了一碗「進階」的《{title}》，問了三題。** 湯面固定顯示在聊天區上方；每個回答第一行都是標記，第二行是老湯的一句話；計分板同步更新。

{qa_block(first3)}

![midgame]({RAW}app_2_midgame.png)

**(3) 按「給點提示」。** 提示者只拿得到關鍵事實清單，所以提示是用「某樣東西／某個人」包裝的一句問句：

> {hint}

![hint]({RAW}app_3_hint.png)

**(4) 繼續問，最後說出完整真相 → 【破案】。** 湯底是由程式接在老湯那句話後面公布的，所以一定和題庫原文一致；計分板變成「✅ 已破案」。

{qa_block(rest)}

![solved]({RAW}app_4_solved.png)

**(5) 換成「困難・AI 現煮」，主題填「捷運」。** 這碗是模型當場用 JSON 出的題《{ai_title}》（{ai_source}）。本機 14B 模型出的題邏輯不算嚴謹，這也是題庫為主、AI 出題為輔的原因。

![ai puzzle]({RAW}app_5_ai_puzzle.png)

**(6) 問一題後按「我放棄，公布湯底」。** 公布湯底不經過模型，直接印出這局的 `truth`。

> {reveal.replace(chr(10), ' ')}

![reveal]({RAW}app_6_reveal.png)
"""
open("tools/sections/shots.md", "w", encoding="utf-8").write(md.strip("\n") + "\n")
print("shots.md written; puzzle:", title, "| AI puzzle:", ai_title, "|", ai_source)
