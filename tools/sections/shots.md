## 8. Gradio 對話結果（實際操作截圖）

截圖是在本機跑 `app.py`（和 notebook 同一份程式，模型 `ollama:qwen2.5:14b`）、用 Playwright 真的點按鈕、打字送出後擷取的；每一張對應的對話全文在 repo 的 `screenshots/app_log.json`。流程：點一碗湯 → 問三題 → 按提示 → 再問到破案 → 換 AI 現煮 → 公布湯底。

**(1) 開店畫面。** 上方選難度、湯從哪來、主題；聊天區是老湯的開場白；下方是問題輸入框與三個功能鍵，最下面是計分板。

![start](https://raw.githubusercontent.com/arvin611ch/taica-lab06-turtle-soup/main/screenshots/app_1_start.png)

**(2) 點了一碗「進階」的《最後一班車》，問了三題。** 湯面固定顯示在聊天區上方；每個回答第一行都是標記，第二行是老湯的一句話；計分板同步更新。第三題「這跟動物有關嗎？」老湯回的是【部分正確】而不是【是】，是小模型判定偏保守的例子（計分板因此多了「部分正確 1」）；這種誤差正是為什麼要把判定做成可統計的標記，才看得出模型哪裡不穩。

> **客人：** 站務員是在練習嗎？  
> **老湯：** 【不是】 練習啊，他都幹這行好幾年了，還用練習喔。  
> **客人：** 廣播是給人聽的嗎？  
> **老湯：** 【不是】 人啊，這時候月台上應該沒人了。  
> **客人：** 這跟動物有關嗎？  
> **老湯：** 【部分正確】 跟動物有關係，但還不夠接近真相。

![midgame](https://raw.githubusercontent.com/arvin611ch/taica-lab06-turtle-soup/main/screenshots/app_2_midgame.png)

**(3) 按「給點提示」。** 提示者只拿得到關鍵事實清單，所以提示是用「某樣東西／某個人」包裝的一句問句：

> 【提示 1/3】 某樣東西是為了叫醒某個人嗎？

![hint](https://raw.githubusercontent.com/arvin611ch/taica-lab06-turtle-soup/main/screenshots/app_3_hint.png)

**(4) 繼續問，最後說出完整真相 → 【破案】。** 湯底是由程式接在老湯那句話後面公布的，所以一定和題庫原文一致；計分板變成「✅ 已破案」。

> **客人：** 牠平常會睡在軌道上？  
> **老湯：** 【是】 嗯，這就更接近了。  
> **客人：** 我知道了：有一隻貓習慣睡在軌道上，站務員每天末班車後廣播，是為了把牠嚇到月台上，免得隔天第一班車撞到牠。  
> **老湯：** 【破案】 哇，你這觀察力不錯嘛，一下子就看穿了。

![solved](https://raw.githubusercontent.com/arvin611ch/taica-lab06-turtle-soup/main/screenshots/app_4_solved.png)

**(5) 換成「困難・AI 現煮」，主題填「捷運」。** 這碗是模型當場用 JSON 出的題《捷運驚魂夜》（AI 現煮）。本機 14B 模型出的題邏輯不算嚴謹，這也是題庫為主、AI 出題為輔的原因。

![ai puzzle](https://raw.githubusercontent.com/arvin611ch/taica-lab06-turtle-soup/main/screenshots/app_5_ai_puzzle.png)

**(6) 問一題後按「我放棄，公布湯底」。** 公布湯底不經過模型，直接印出這局的 `truth`。

> 🍲 湯底公布： 這名乘客患有雙重人格症，在夜間當他的人格轉換發生時，另一個他在車廂內低語與他對話，只是他自己並不知道。

![reveal](https://raw.githubusercontent.com/arvin611ch/taica-lab06-turtle-soup/main/screenshots/app_6_reveal.png)
