# 🌕 中秋小遊戲樂園 (Mid-Autumn Games Arcade)

> 一個以中秋佳節為主題、採用 **FastAPI + HTMX + TailwindCSS** 打造的沉浸式互動遊戲大廳。零 npm、零手寫 JavaScript、純 Python 驅動的現代 SPA 架構！

---

## 🔗 Demo

🌐 **公開線上展示網址 (Vercel / Production)**:  
👉 **[https://moon-festival-homework.vercel.app](https://moon-festival-homework.vercel.app)** *(可依你的實際 Vercel 專案網址更新)*

---

## ✨ 作品亮點與架構特色

* **⚡ 現代 Python HOT 棧**：採用 **FastAPI + HTMX + TailwindCSS**，徹底摒棄繁雜的 Node.js/npm 建置流程與手寫 JavaScript。
* **🎨 質感圖標系統 (Lucide Icons)**：引入官方 Lucide CDN，結合 HTMX 的 `hx-on::after-swap` 事件，在零手寫 JS 的架構下實現流暢動態圖標渲染。
* **🎮 遊戲大廳 Hub + 雙款獨立 SPA 模式**：
  * **大廳首頁 (`/`)**：沉浸式中秋夜空星月視覺，導引玩家至各個獨立小遊戲。
  * **第一款遊戲：月餅點點樂 (`/games/mooncake`)**：點擊烘烤月餅、購買自動烤爐與玉兔助手、達成烘焙成就。
  * **第二款遊戲：露天烤肉模擬器 (`/games/bbq`)**：掌握火候、翻面、刷烤肉醬、起鍋享用，避免烤焦挑戰最高美味分！
* **🔄 HTMX 局部動態交換**：藉由 `hx-post`、`hx-target` 與 `hx-swap` 進行局部 DOM 替換，點擊時畫面無閃爍、即時更新分數與按鈕狀態。
* **🎨 Tailwind Play CDN**：免裝 npm，透過官方 CDN 實現節慶金夜漸層、發光滿月與流暢縮放動畫。
* **📐 嚴格遵循 SDD (規格驅動) 與 TDD (測試驅動)**：核心引擎與 API 路由皆具備自動化測試，25 項測試 100% 綠燈覆蓋。

---

## 📁 檔案結構 (Repository Structure)

```text
moon-festival-homework/
├── DESCRIPTION.md            # 作業題目與評分標準
├── SPEC.md                   # SDD 規格書 (玩法、API 路由、驗收標準)
├── INCIDENT.md               # AI 協作故障覆盤記錄 (Post-Mortem)
├── RETROSPECTIVE.md          # AI 協作反思報告 (回答 6 大問題)
├── README.md                 # 專案介紹與執行指南 (本文件)
├── requirements.txt          # Python 相依套件 (FastAPI, Uvicorn, Jinja2, etc.)
├── vercel.json               # Vercel 一鍵部署設定
├── main.py                   # FastAPI 應用入口與大廳路由
├── app/
│   ├── games/
│   │   ├── mooncake/         # 第一款遊戲：月餅點點樂
│   │   │   ├── engine.py     # 核心業務邏輯
│   │   │   └── router.py     # API 路由與 HTMX 端點
│   │   └── bbq/              # 第二款遊戲：露天烤肉模擬器
│   │       ├── engine.py     # 烤爐雙面熟成度計算引擎
│   │       └── router.py     # 烤肉 API 端點 (place, flip, sauce, serve)
│   └── templates/
│       ├── base.html         # 全站基底模板 (Tailwind, HTMX & Lucide CDN)
│       ├── index.html        # 遊戲大廳首頁 (Hub)
│       └── games/
│           ├── mooncake.html # 月餅點點樂頁面
│           ├── bbq.html      # 露天烤肉模擬器頁面
│           └── partials/
│               ├── game_state.html # 月餅點點樂 HTMX 片段
│               └── bbq_state.html  # 烤肉模擬器 HTMX 片段
└── tests/
    ├── test_engine.py        # 月餅邏輯單元測試 (TDD)
    ├── test_api.py           # 月餅 API 端點測試 (TDD)
    ├── test_bbq.py           # 烤肉核心引擎單元測試 (TDD)
    └── test_bbq_api.py       # 烤肉 API 端點整合測試 (TDD)
```

---

## 🚀 本地開發與執行 (Development)

專案完全不需安裝 npm！電腦具備 Python 3.9+ 即可直接運行。

### 1. 建立虛擬環境並安裝相依套件
```bash
# 建立虛擬環境
python3 -m venv .venv

# 啟動虛擬環境 (macOS / Linux)
source .venv/bin/activate

# 安裝極簡相依套件 (FastAPI, Uvicorn, Jinja2, httpx)
pip install -r requirements.txt
```

### 2. 執行自動化測試 (TDD 驗證)
驗證雙遊戲核心計分邏輯、雙面熟成判定與所有 API 路由端點：
```bash
.venv/bin/python -m unittest discover tests
```
> 輸出 `Ran 25 tests in 0.05s - OK` 即代表核心邏輯與 API 全部通過！

### 3. 本地啟動伺服器 (Local Run)
```bash
.venv/bin/uvicorn main:app --reload --port 8000
```
在瀏覽器打開：`http://127.0.0.1:8000` 即可暢玩遊戲大廳、月餅點點樂與露天烤肉模擬器！

---

## 🤖 AI Tools & 協作模式 (AI Collaboration)

* **主要 AI 助理**：**Antigravity (Powered by Gemini 3.8)**
* **協作流程**：
  1. **Specification (規格)**：先制定 [SPEC.md](file:///Users/alexh/Projects/School/moon-festival-homework/SPEC.md)，明確定義端點、玩法與驗收標準。
  2. **TDD (測試)**：編寫 [tests/test_engine.py](file:///Users/alexh/Projects/School/moon-festival-homework/tests/test_engine.py) 與 [tests/test_api.py](file:///Users/alexh/Projects/School/moon-festival-homework/tests/test_api.py)，經由紅燈驗證後再完成實作轉為綠燈。
  3. **Verification & Post-Mortem (覆盤)**：捕捉 AI 生成測試時的狀態突變錯誤，詳載於 [INCIDENT.md](file:///Users/alexh/Projects/School/moon-festival-homework/INCIDENT.md)。
  4. **Retrospective (回顧)**：詳載於 [RETROSPECTIVE.md](file:///Users/alexh/Projects/School/moon-festival-homework/RETROSPECTIVE.md)。

---

## 🚢 部署至 Vercel (Deployment)

本專案已包含標準 `vercel.json`：
1. 將代碼推送到 GitHub Repository。
2. 登入 [Vercel](https://vercel.com/)，點擊 **Add New Project** 並 Import 此 Repository。
3. 保持預設設定，點擊 **Deploy**，Vercel 將自動建立 Serverless Python 環境並產生正式網址！
