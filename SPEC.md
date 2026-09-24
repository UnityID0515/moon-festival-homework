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

---

## 5. 第二階段功能規格：中秋露天烤肉模擬器 (Moonlit BBQ Simulator)

### 5.1 核心玩法機制 (Core Mechanics)
1. **烤網工位 (Grill Slots)**：
   * 烤爐提供 **3 個獨立烤位**（Slot 0, 1, 2）。
   * 每個烤位可處於：`空置 (empty)` 或 `烤製中 (cooking)`。
2. **食材種類 (Food Types)**：
   * **牛肉串 (beef)**：熟成速度 10%/秒，基礎分 100 分。
   * **甜不辣 (tempura)**：熟成速度 15%/秒，基礎分 80 分。
   * **經典香腸 (sausage)**：熟成速度 8%/秒，基礎分 120 分。
3. **雙面受熱與翻面 (Dual-side Doneness & Flip)**：
   * 烤物有 **正面 (Side A)** 與 **反面 (Side B)** 兩個熟成進度 (0% ~ 100%+)。
   * 放上烤網時預設為正面接觸火源。
   * 點擊「翻面 (`POST /games/bbq/flip/{slot_id}`)」切換受熱面。
4. **刷烤肉醬 (Brush Sauce)**：
   * 點擊「刷醬 (`POST /games/bbq/sauce/{slot_id}`)」為烤物增添風味，享用時得分獲得 **1.5 倍加成**（每串限刷一次）。
5. **起鍋享用 (Serve / Eat)**：
   * 點擊「起鍋 (`POST /games/bbq/serve/{slot_id}`)」評定熟成度並獲取美味積分：
     * **完美熟成 (Perfect)**：正面與反面熟度皆在 60% ~ 100% 之間。獲得 `基礎分 * 醬料加成`。
     * **夾生生肉 (Raw)**：任一面熟度 < 60%。獲得 0 分，提示「太生了！吃了會拉肚子！」。
     * **烤焦焦炭 (Burnt)**：任一面熟度 > 100%。獲得安慰分 10 分，提示「烤焦了！苦苦的...」。
6. **定時受熱 (Tick)**：
   * 前端使用 HTMX `hx-trigger="every 1s"` 定時呼叫 `POST /games/bbq/tick`，當前受熱面增加該食材之熟成進度。

---

## 6. 驗收標準 (Acceptance Criteria)

- [ ] **AC-1 (大廳與導航)**：訪問 `/` 正常顯示遊戲大廳，具備典雅中秋夜空視覺與遊戲卡片，點擊可無縫進入 `/games/mooncake` 與 `/games/bbq`。
- [ ] **AC-2 (月餅點點樂)**：點擊月餅透過 HTMX 局部更新分數，升級與被動每秒累積正常。
- [ ] **AC-3 (烤肉槽位操作)**：玩家可將牛肉串、甜不辣、香腸放上指定烤位，翻面正確切換受熱面。
- [ ] **AC-4 (烤肉熟成與刷醬結算)**：每秒正確推進受熱面熟度，雙面熟成判定（完美、夾生、烤焦）與 1.5 倍刷醬加成計算無誤。
- [ ] **AC-5 (會話隔離與無刷新)**：所有操作透過 HTMX 局部更新，不同玩家狀態透過 Session 隔離。
- [ ] **AC-6 (無 npm / 無 hand-written JS)**：全專案無 `package.json`，不手寫 JS 檔案。
- [ ] **AC-7 (TDD 測試全數通過)**：執行 `python -m unittest` 時，所有遊戲引擎與 API 測試 100% 通過。

---

## 7. 非目標 (Non-goals)

* 本階段不串接外部付費關聯式資料庫（採用高效能 Session 狀態）。
* 本階段不引入前端打包管線（如 Webpack / Vite / PostCSS）。
