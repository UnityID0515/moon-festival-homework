# 📝 AI 協作回顧報告 (AI Collaboration Retrospective)

本報告記錄在中秋 H5 開發專案中，身為工程新手（Noob）透過 **SDD (規格驅動開發)** 與 **TDD (測試驅動開發)** 引導 AI 進行開發的反思與總結。

---

### 1. 你用了哪些 AI / Agent？
* **Antigravity (Powered by Gemini 3.8)**：作為主要 Coding Agent，負責分析作業需求、架構諮詢、實作 FastAPI 後端、HTMX 動態交換模板、Tailwind CSS 排版與撰寫自動化測試。

---

### 2. AI 做得最好的一件事是什麼？
* **零 JS / 零 npm 的架構轉型與諮詢 (Architecture & Stack Consultation)**：
  當我提出「不想要 npm、不寫 JavaScript、希望以 Python 為核心打造 Hub + SPAs」的需求時，AI 提供了客觀專業的架構評估，並精確採用了現代 Python 生態中最火紅的 **HOT 棧 (FastAPI + HTMX + TailwindCSS via CDN)**。
  此外，在視覺設計迭代上，AI 透過官方 CDN 整合了 **Lucide Icons**，搭配 HTMX 的 `hx-on::after-swap` 事件，在堅持「零手寫 JS 與零 npm」的前提下，讓遊戲大廳與月餅點點樂獲得了現代高質感的 SVG 向量圖標與流暢的動態置換體驗。
  在第二階段拓展「中秋露天烤肉模擬器」時，得益於 Hub 模組化設計與 TDD 規範，僅用極短時間便以純 Python 實作出雙面受熱模型與 HTMX 烤爐互動，並新增 13 項測試確保零回歸（Zero Regressions）。


---

### 3. AI 搞砸的一件事是什麼？
* **狀態突變時序理解偏差 (State Mutation Race Condition)**：
  在編寫每秒被動產能（CPS）的測試時，AI 忽略了「執行購買操作後，道具價格會立即根據指數倍率上升」的規則，在斷言時直接使用了購買後的新價格來計算歷史消耗，導致測試結果出現數值偏差（詳見 [INCIDENT.md](file:///Users/alexh/Projects/School/moon-festival-homework/INCIDENT.md)）。

---

### 4. 你怎麼發現它錯了？
* **嚴格落實 TDD (Test-Driven Development) 與自動化測試**：
  在啟動伺服器之前，我先在本機終端機執行：
  ```bash
  .venv/bin/python -m unittest discover tests
  ```
  測試套件立即亮出紅燈報錯，精確指出哪一行測試斷言失敗，而不是等到瀏覽器畫面跑出來、玩家發現數字怪怪的才去手動除錯。

---

### 5. 最後怎麼解決？
* **釐清動態計算屬性並顯式緩存初始值**：
  我要求 AI 審視狀態變更的先後順序，在觸發購買動作前先行記錄 `initial_cost` 快照，並將斷言邏輯修改為以該快照為基準進行累加。修正後再次執行單元測試，全部 12 項測試全數通過（綠燈）。

---

### 6. 如果重做一次，你會怎麼改變自己的 AI 協作方式？
* **從一開始就明確定義 Deployment Platform 與後端邊界**：
  最初由於先入為主地設定在純前端靜態主機，導致走了一小段純前端 Python (Brython) 的彎路；若重做一次，我會在最初的溝通中就明確提出「多遊戲 Hub」與「後端架構偏好」，直接進入 FastAPI + HTMX 的正式架構，省去中間換棧的時間成本。
