# AI 協作紀錄（依作業註三）

本作業在 **Claude Code**（Anthropic Claude，終端機裡的程式協作工具）協作下完成；人設討論另外用本機 Ollama 的 **Qwen2.5-14B**（四輪對話的截圖與全文在 notebook §1 與 `screenshots/design_chat_*.png`、`screenshots/design_chat_log.json`）。

## 給 Claude Code 的要求

1. 貼上第六週作業說明（用 aisuite 打造自己的對話機器人、Gradio 展示、繳交內容、評分標準、註一至註四），要求在 `taica_gen_ai/lab6` 完成整份作業。
2. 要求一切照作業規定：保留老師固定套件、主題不能跟老師範例相似、有用 AI 的地方要說明並附 prompt 與結果截圖。

## Claude Code 做的事（依時間順序）

1. 下載並閱讀老師的三份範例 notebook（用 AISuite 打造員瑛式思考生成器新版、用 OpenAI API 打造自己的對話機器人、用 aisuite 輕鬆使用多個 LLM），整理出固定套件、金鑰讀法、`reply` 函數與 Gradio 寫法。
2. 確認本機可用的模型：沒有可用的雲端 API 金鑰，改用本機 Ollama 的 Qwen2.5-14B 透過 aisuite 的 `ollama:` 供應商測試；Colab 版改讀 Colab 🔑 的 Groq／OpenRouter／OpenAI／Anthropic 金鑰。
3. 決定主題：海龜湯主持人「老湯」（要藏祕密、照固定格式回是非題、判斷破案、多輪有狀態），刻意避開「風格改寫」類型。
4. 寫最陽春的聊天室 `tools/design_chat_app.py`，用 Playwright（`tools/shoot_design_chat.py`）實際送出四輪提問給 Qwen2.5-14B 並截圖。
5. 撰寫三段 prompt（主持人、出題者、提示者）、6 題原創題庫、核心函式、文字版測試（正常一局、防洩題、提示與 AI 現煮）、統計圖、Gradio Blocks 介面；全部放在 `tools/build_notebook.py`，由它產生 notebook 與 `app.py`。
6. 先用 `app.py` 做格式冒煙測試（三句：是非題、耍賴、完整真相），確認模型會輸出【標記】且程式能解析、破案時由程式公布湯底。
7. 用 nbclient 從頭執行 notebook 產生所有輸出；同時啟動 Gradio，用 Playwright（`tools/shoot_app.py`）實際點湯、問問題、按提示、破案、AI 現煮、公布湯底並截圖。
8. 建立 GitHub repo、推上 notebook 與截圖，產生 Colab 連結與繳交文字。

## 測試中發現並修正的事

- Qwen2.5-14B 對「海龜湯」的認知是錯的（以為是描述詞語猜謎），因此 prompt 把玩法與判定規則全部寫明，不依賴模型既有知識。
- 討論人設時 AI 第 2、3 輪的版本缺少：明確的破案標準、程式可判讀的標記格式、防注入規則、提示機制；定稿 prompt 逐一補上。
- 用 uv 建立的虛擬環境沒有 pip，`!pip install` 會失敗，補裝 pip；Playwright 既有 chromium 為 ARM 版，改 `PLAYWRIGHT_BROWSERS_PATH` 重裝 x86 版。
