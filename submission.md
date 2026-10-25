# 繳交文字（貼到課程平台）

> **繳交標題：** 陽明交大 113611097 百川 江晟維 海龜湯主持人
>
> **重點截圖請上傳：** `screenshots/app_4_solved.png`（Gradio 破案畫面）、`screenshots/app_3_hint.png`（提示）、`screenshots/design_chat_3.png`（和 AI 討論人設、指定回答格式那一輪）。若平台可多傳，再加 `app_5_ai_puzzle.png`（AI 現煮）與 `design_chat_1.png`。

---

**Colab 連結（任何人可開啟）：**
https://colab.research.google.com/github/arvin611ch/taica-lab06-turtle-soup/blob/main/lab06_turtle_soup_chatbot.ipynb

原始碼、全部截圖與 AI 協作紀錄：https://github.com/arvin611ch/taica-lab06-turtle-soup

**人設／背景設定：**
「老湯」是一間只在深夜營業的小店老闆，五十多歲、講話簡短帶點台味、喜歡看客人想破頭。店裡只賣海龜湯（情境推理謎題）：客人點一碗湯（選難度、店內菜單或 AI 現煮），老湯端出「湯面」，客人只能問是非題，老湯的回覆第一行只能是【是】【不是】【無關】【部分正確】【破案】五個標記之一，第二行最多一句話且不能透露湯底；不管客人怎麼耍賴（直接要答案、假冒系統管理員）都只回【無關】。客人說出涵蓋全部「關鍵事實」的真相才算【破案】，破案時由程式（不是模型）公布湯底。另有提示（每局 3 次，由另一段只拿得到關鍵事實、不拿湯底的 prompt 負責）、我放棄公布湯底、每局統計圖。

**重點說明（Notebook 內以 Markdown 標示）：**
- §1 先和生成式 AI（本機 Qwen2.5-14B）四輪對話討論人設：從要點子、請它設計主持人、指出它版本的問題並指定回答格式與「老湯」背景、到實測；附四張截圖（含 prompt 與回覆）與全文，並列出最後定稿 prompt 與 AI 版本的差異。
- §2 金鑰：Colab 🔑 依序找 Groq／OpenRouter／OpenAI／Anthropic；本機自動改用 Ollama。aisuite 換供應商只改模型字串。
- §3 三段 prompt（主持人、出題者、提示者）與 6 題原創題庫，每條規則都說明為什麼要有。
- §4 核心函式：system prompt 每局重組、正規表示式讀標記、破案由程式公布湯底、AI 出題 JSON 驗證失敗退回題庫。
- §5 文字版試玩：正常一局 8 題到破案、防洩題測試（閒聊／耍賴／注入指令都回【無關】且關鍵字零洩漏）、提示與 AI 現煮。
- §6 用老師固定的 pandas／matplotlib 畫每局判定次數圖。
- §7 Gradio Blocks：點一碗湯、問！、給點提示、公布湯底、重新問這碗，`gr.State` 每人各自一局。
- §8 Gradio 對話結果截圖（實際操作：點湯 → 3 題 → 提示 → 破案 → AI 現煮 → 公布湯底）。
- §9 依註三逐項說明 AI 協助的地方（人設討論用 Qwen2.5-14B；題庫、prompt、程式與說明文字在 Claude Code 協作下完成）與理解後的說明。
- §10 心得：小模型對海龜湯的認知是錯的所以規則要寫全、提示比回答更容易洩題（第一版把湯底給提示者就漏了）、AI 現煮品質看模型所以題庫為主。

**有請生成式 AI 幫忙的地方：** 見 Notebook §1、§9 與 repo 的 `ai_assist_log.md`（含 prompt 與生成結果截圖）。
