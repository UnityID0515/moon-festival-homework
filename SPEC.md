# 🌕 中秋小遊戲樂園 (Mid-Autumn Games Arcade) - SPECIFICATION (SDD)

本專案遵循 **SDD (Spec-Driven Development，規格驅動開發)** 流程。在編寫程式碼之前，先定義清楚需求、架構、API 行為、驗收標準（Acceptance Criteria）與 Non-goals。

---

## 1. 專案願景與目標 (Vision & Goals)

* **主題**：以中秋節（Mid-Autumn Festival）文化為核心的互動遊戲大廳。
* **目標受眾**：希望體驗節慶氛圍、輕鬆遊玩小遊戲的玩家。
* **架構定位**：**遊戲大廳 Hub + 獨立小遊戲 SPA 模式**。
  * **遊戲大廳 (`/`)**：典雅中秋夜空氛圍，導引玩家至各個獨立小遊戲。
  * **第一款遊戲 (`/games/mooncake`)**：**🌕 月餅點點樂 (Mooncake Clicker)** —— 經典放置型休閒點擊遊戲。
  * **擴充性**：預留後續中秋烤肉模擬器、天燈祈福等獨立 SPA 模組之接入路徑。

---

## 2. 技術棧與規範 (Tech Stack)

* **後端架構**：**Python 3 + FastAPI + Uvicorn**
  * 高效能、非同步支援、乾淨現代的 Python Web 框架。
  * 支援以 `fastapi.testclient.TestClient` 執行標準單元測試（TDD）。
* **前端動態互動**：**HTMX (via CDN)**
  * **零手寫 JavaScript、零 npm / Node.js 建置流程**。
  * 透過 HTML 屬性（`hx-post`, `hx-target`, `hx-swap`）實現局部 DOM 替換，達到無刷新 SPA 體驗。
* **前端視覺樣式**：**TailwindCSS (via Play CDN)**
  * 透過官方 CDN `<script src="https://cdn.tailwindcss.com"></script>` 載入。
  * 零安裝、響應式排版，打造沉浸式中秋節慶夜空與月餅動畫。
* **圖標系統 (Iconography)**：**Lucide Icons (via CDN)**
  * 透過官方 CDN `<script src="https://unpkg.com/lucide@latest"></script>` 載入。
  * 搭配 HTMX `hx-on::after-swap="lucide.createIcons()"` 達成局部置換後的自動圖標渲染，提供現代且專業的向量圖標。
* **模板引擎**：**Jinja2**
  * 支援全頁渲染（Full Page）與 HTMX 局部片段（Partial HTML）無縫共用。
* **部署平台**：**Vercel / Render**（具備 `vercel.json` 一鍵部署配置）。

---

## 3. 系統架構與檔案結構 (Project Structure)

```text
moon-festival-homework/
├── DESCRIPTION.md            # 作業需求說明文件
├── SPEC.md                   # 系統規格書 (本文件)
├── INCIDENT.md               # AI 協作故障覆盤記錄 (Post-Mortem)
├── RETROSPECTIVE.md          # AI 協作反思報告 (回答 6 大問題)
├── README.md                 # 專案介紹、展示連結與本地執行指南
├── requirements.txt          # Python 相依清單 (FastAPI, Uvicorn, Jinja2, etc.)
├── vercel.json               # Vercel 一鍵部署設定檔
├── main.py                   # FastAPI 應用入口與全域路由
├── app/
│   ├── __init__.py
│   ├── games/
│   │   ├── __init__.py
│   │   └── mooncake/
│   │       ├── __init__.py
│   │       ├── engine.py     # 純 Python 業務邏輯核心 (計分、升級、成就)
│   │       └── router.py     # 月餅遊戲路由與 HTMX 端點
│   └── templates/
│       ├── base.html         # 全站基底 (載入 Tailwind & HTMX CDN)
│       ├── index.html        # 遊戲大廳首頁 (Hub)
│       └── games/
│           ├── mooncake.html # 月餅點點樂 SPA 完整頁面
│           └── partials/     # HTMX 局部替換片段
│               ├── stats.html       # 分數與產能看板
│               ├── upgrades.html    # 升級道具卡片清單
│               └── achievements.html# 成就解鎖狀態
└── tests/
    ├── __init__.py
    ├── test_engine.py        # 核心遊戲邏輯單元測試 (TDD)
    └── test_api.py           # FastAPI 端點整合測試 (TDD)
```

---

## 4. 第一階段功能規格：月餅點點樂 (Mooncake Clicker)

### 4.1 核心玩法機制 (Core Mechanics)
1. **點擊月餅 (Active Click)**：
   * 玩家點擊畫面上大月餅按鈕，發送 `POST /games/mooncake/click`。
   * 後端增加使用者之月餅數量 `+cpc`（每次點擊增加量），初始 `cpc = 1`。
   * HTMX 局部更新畫面分數看板（`#stats-panel`）與道具購買按鈕狀態。
2. **自動生產 (Passive Generation / CPS)**：
   * 道具提供每秒自動烘烤產能 `cps`。
   * 前端使用 HTMX `hx-trigger="every 1s"` 定時觸發 `POST /games/mooncake/tick`，自動結算被動產量並刷新看板。
3. **升級道具系統 (Upgrades)**：
   * 玩家發送 `POST /games/mooncake/buy/{item_id}` 購買升級。
   * **玉兔搗藥杵 (mortar)**：基礎造價 15，點擊產能 +1，價格係數 1.15。
   * **廣寒宮烤箱 (oven)**：基礎造價 50，每秒產能 +1，價格係數 1.15。
   * **金沙鹹蛋黃 (yolk)**：基礎造價 200，點擊產能 +5，價格係數 1.20。
   * **嫦娥仙氣 (blessing)**：基礎造價 800，每秒產能 +10，價格係數 1.25。
   * 價格遞增公式：`cost = floor(base_cost * (multiplier ^ count))`。
4. **成就系統 (Achievements)**：
   * 累計產量達 10、100、1000、10000 顆時解鎖稱號徽章。
5. **進度重設 (Reset)**：
   * 提供 `POST /games/mooncake/reset` 將遊戲重置回初始狀態。

---

## 5. 驗收標準 (Acceptance Criteria)

- [ ] **AC-1 (大廳與導航)**：訪問 `/` 正常顯示遊戲大廳，具備典雅中秋夜空視覺與遊戲卡片，點擊可無縫進入 `/games/mooncake`。
- [ ] **AC-2 (點擊互動)**：點擊月餅按鈕時，透過 HTMX 局部更新分數，月餅數量嚴格按 `cpc` 累加，頁面不發生整頁重新載入。
- [ ] **AC-3 (升級機制)**：當月餅不足時，購買按鈕呈現 disabled 狀態或購買失敗；月餅充足時扣除對應月餅數，提升產能，道具價格依指數公式向上遞增且維持整數。
- [ ] **AC-4 (定時被動產能)**：網頁開啟時，每秒自動觸發一次 tick，月餅數量自動按 `cps` 增加。
- [ ] **AC-5 (會話隔離)**：不同瀏覽器或使用者訪問時，各自擁有獨立遊戲狀態（透過 Cookie Session 區隔）。
- [ ] **AC-6 (無 npm / 無 hand-written JS)**：專案內無 `package.json`、無 `node_modules`，不需手寫任何 JavaScript 檔案。
- [ ] **AC-7 (TDD 測試全數通過)**：執行 `pytest` 或 `python3 -m unittest` 時，核心引擎與 API 端點測試 100% 通過。

---

## 6. 非目標 (Non-goals)

* 本階段不串接外部付費關聯式資料庫（採用高效能 Session 狀態）。
* 本階段不引入前端打包管線（如 Webpack / Vite / PostCSS）。
