# 🚨 AI Collaboration Incident Post-Mortem (AI 協作故障覆盤記錄)

本文件依據作業要求，忠實記錄在專案開發過程中發生的 **AI 產出錯誤、如何透過測試/審查發現、以及流程修正** 的事後分析（Post-Mortem）。

---

## 案例一：升級道具動態調價與測試斷言時序錯誤 (State Mutation Race Condition)

### 1. 我想要什麼 (Requirement)
驗證遊戲的「每秒被動產能 (CPS, Cakes Per Second)」累積邏輯：
* 購買「廣寒宮烤箱」（基礎造價 50 月餅，每秒自動產出 +1 顆）。
* 模擬時間經過 2 秒鐘。
* 驗證月餅總生產量（`total_produced`）應等於：`購買時消耗成本 + (CPS * 經過秒數)`。

### 2. AI 做了什麼 (AI Behavior & Failure)
AI 撰寫了如下的測試代碼：
```python
oven = self.game.upgrades["oven"]
self.game.score = oven.cost
self.game.total_produced = oven.cost
self.game.buy_upgrade("oven")       # ⚠️ 這裡觸發了 oven.count += 1
self.assertEqual(self.game.cps, 1)

earned = self.game.tick(2.0)
self.assertEqual(self.game.total_produced, oven.cost + 2) # ❌ 錯誤所在
```

### 3. 我怎麼發現它錯了 (Detection via TDD)
執行單元測試 `python -m unittest discover tests` 時，測試直接亮紅燈爆出錯誤：
```text
FAIL: test_passive_tick (test_engine.TestMooncakeEngine)
AssertionError: 52 != 59
```
實際產出的總量為 `52`，但斷言計算出來卻是 `59`。

### 4. 根本原因分析 (Root Cause Analysis)
* 根據規格定義：道具價格是**動態計算屬性（Computed Property）**，公式為 `cost = floor(base_cost * 1.15^count)`。
* 烤箱初始價格為 50。
* 當執行 `buy_upgrade("oven")` 後，烤箱持有數變為 1，此時 `oven.cost` 立即被重新計算為 `57`！
* AI 在最後斷言時，直接讀取了購買後的變動屬性 `oven.cost` (57)，加上 2 變成了 `59`，忽略了狀態突變（State Mutation）的副作用！

### 5. 怎麼解決 (Resolution)
1. **規格與測試修正**：在觸發購買動作前，顯式建立快照（Snapshot）記錄 `initial_cost`。
2. **修正後代碼**：
   ```python
   initial_cost = oven.cost
   self.game.score = initial_cost
   self.game.total_produced = initial_cost
   self.game.buy_upgrade("oven")
   self.assertEqual(self.game.total_produced, initial_cost + 2)
   ```
3. 重新執行 `unittest`，測試立即綠燈通過。

---

## 案例二：Template 標籤結構與測試斷言字串不一致 (DOM Tag Mismatch)

### 1. 我想要什麼
驗證使用者呼叫 `POST /games/mooncake/reset` 重設遊戲時，後端回傳的 HTMX 局部片段能正確將累計產量歸零。

### 2. AI 做了什麼
AI 在 API 整合測試 `tests/test_api.py` 中寫道：
```python
reset_res = self.client.post("/games/mooncake/reset", cookies=cookies)
self.assertIn("累計產量: 0", reset_res.text) # ❌ 假設是純文字
```

### 3. 我怎麼發現它錯了
執行 `tests/test_api.py` 時回報失敗：
```text
FAIL: test_reset_endpoint (tests.test_api.TestMooncakeAPI)
AssertionError: '累計產量: 0' not found in '<div id="stats-panel">...累計總產量: <span class="...">0</span> 顆...'
```

### 4. 根本原因
HTML 模板中使用了語意化標籤，將數字包裝在 `<span class="font-mono text-slate-200">0</span>` 中以利 Tailwind 渲染樣式，且中文文案為「累計總產量:」，導致嚴格的字串包含比對失敗。

### 5. 怎麼解決
修改測試斷言，分開驗證文案語意與數字節點：
```python
self.assertIn("累計總產量", reset_res.text)
self.assertIn(">0</span>", reset_res.text)
```
測試順利全數通過。

---

## 💡 協作心得與反思 (Takeaways)
1. **自動化測試是 AI 協作的唯一真理**：若沒有 TDD 單元測試，數值計算與動態調價的 Bug 很可能會悄悄流入正式環境，直到玩家遊玩時才被發現。
2. **AI 擅長架構搭建，但邊界時序容易疏忽**：AI 能在幾秒內寫出乾淨的 FastAPI 與 HTMX 架構，但在「先購買還是先記錄數值」、「DOM 標籤的字串比對」等細節上，依然需要工程師把關審查。
