# TAICA 生成式 AI｜Lab 06：用 aisuite 打造「深夜海龜湯店老闆：老湯」對話機器人

陽明交大 113611097 百川 江晟維

- **Colab：** https://colab.research.google.com/github/arvin611ch/taica-lab06-turtle-soup/blob/main/lab06_turtle_soup_chatbot.ipynb
- **Notebook（含執行結果）：** `lab06_turtle_soup_chatbot.ipynb`
- **截圖：** `screenshots/`（`design_chat_*.png` 是和 AI 討論人設的四輪對話；`app_*.png` 是 Gradio 實際操作）
- **AI 協作紀錄：** `ai_assist_log.md`

## 作品是什麼

老湯是一間只在深夜營業的小店老闆，店裡只賣「海龜湯」（情境推理謎題）。客人點一碗湯，老湯端出「湯面」，客人只能問是非題，老湯只回【是】【不是】【無關】【部分正確】【破案】；客人說出涵蓋全部關鍵事實的真相才算破案，破案時由程式公布湯底。

和老師範例（單輪風格改寫）不同的地方：機器人要**守住祕密**、**照固定格式回答**（程式用正規表示式判讀、計分）、**判斷是否破案**、**多輪有狀態**（`gr.State`）。另外有 6 題原創題庫、AI 現煮出題（JSON 驗證＋退回）、提示（限 3 次、另一段 prompt、不給湯底）、每局統計圖。

## 怎麼跑

**Colab**：開上面的連結 → 左側 🔑 新增金鑰（名稱 `Groq`，或 `OpenRouter`／`OpenAI`／`Anthropic`）並打開筆記本存取權 → 全部執行。最後一格會開 Gradio 網頁。

**本機**（需要 Python 3.12）：

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python "aisuite[openai,groq,anthropic]" gradio
export GROQ_API_KEY=...            # 或在本機跑 Ollama，程式會自動改用 ollama:qwen2.5:14b
.venv/bin/python app.py           # http://127.0.0.1:7862
```

`app.py` 是由 `tools/build_notebook.py` 從 notebook 的程式格產生的，兩邊程式一致。

## 檔案

| 檔案 | 用途 |
|---|---|
| `lab06_turtle_soup_chatbot.ipynb` | 作業本體（已在本機用 Ollama Qwen2.5-14B 執行過一次，輸出都在裡面） |
| `app.py` | 獨立可跑的 Gradio 版本 |
| `tools/build_notebook.py` | 產生 notebook 與 app.py |
| `tools/design_chat_app.py`、`tools/shoot_design_chat.py`、`tools/design_prompts.json` | 和 AI 討論人設用的聊天室與自動截圖 |
| `tools/shoot_app.py` | 用 Playwright 實際操作 Gradio 並截圖 |
| `screenshots/*.png`、`screenshots/*.json` | 截圖與對話全文 |
| `ai_assist_log.md` | 依作業註三說明 AI 協作內容 |
