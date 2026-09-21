# 🌕 中秋 H5 × AI 協作開發

請製作一個以「中秋節」為主題的 H5 網頁，並部署到公開網址。

題材不限，例如：

* 中秋賀卡
* 月餅 Clicker
* 烤肉模擬器
* 月相模擬
* 互動故事
* 任何你覺得有趣的東西

作品不用很大，但希望最後是一個**完整、可以分享給別人玩的成品**。

---

## 🎯 這次真正要練習的東西

這份作業不是在比誰最會手刻 HTML / CSS / JavaScript。

你要練習的是：

> **如何定義需求、把工作交給 AI、驗證結果，最後把產品交付出去。**

你的主要工作應該是：

```text
Specification
↓
Delegation
↓
Review
↓
Verification
↓
Delivery
```

Implementation 可以大量交給 AI。

---

# 必做要求

## 1. 中秋主題 H5 網頁

技術不限。

可以使用：

* HTML / CSS / JavaScript
* React
* Vue
* Svelte
* Astro
* 其他 framework

請確保自己知道：

* 專案怎麼跑
* 怎麼 build
* 怎麼 deploy
* 主要功能怎麼運作

---

## 2. 部署到公開網址

最低要求：

* GitHub Pages

也可以使用：

* Cloudflare Pages
* Cloudflare Workers
* Vercel
* Netlify
* 其他服務

README 必須放上可以直接開啟的 Demo URL。

---

## 3. 使用 SDD 或 TDD

### SDD

Repository 中加入：

```text
SPEC.md
```

至少描述：

* 要做什麼
* 主要功能
* 系統行為
* Acceptance Criteria
* Non-goals

建議流程：

```text
Idea
↓
Spec
↓
AI Implementation
↓
Review
↓
修改 Spec
↓
再次實作
```

---

### TDD

先寫測試，再實作。

建議流程：

```text
Test
↓
Fail
↓
AI Implementation
↓
Pass
↓
Refactor
```

至少要測試一些真正的程式行為，例如：

* 計分邏輯
* 遊戲規則
* 狀態轉換
* localStorage
* API
* validation

不要寫沒有實際意義的測試來湊數。

---

# 🤖 AI 使用規則

這次鼓勵你：

> **盡量不要自己寫大量 implementation code。**

可以使用任意 AI / Coding Agent，例如：

* ChatGPT
* Claude
* Claude Code
* Codex
* GitHub Copilot
* Gemini
* Cursor
* Pi
* 其他工具

你主要負責：

* 寫需求
* 寫 Spec / Test
* Prompt
* Review diff
* Debug
* 驗證功能
* 決定 architecture
* 判斷 AI 做得對不對

---

## 可以自己改 Code 嗎？

可以。

這不是「禁止碰程式碼」。

如果你知道一個問題只需要手動改一兩行，就直接改。

但你應該知道：

> **自己為什麼要改，以及 AI 為什麼沒有處理好。**

---

# Git 要求

請保留正常的開發紀錄。

不要最後才：

```bash
git add .
git commit -m "homework"
```

整個 repository 只有一個 commit。

希望 commit history 大致看得出開發過程，例如：

```text
add initial spec
implement mooncake counter
add persistence
fix score bug
deploy to github pages
```

推薦 workflow：

```text
讓 Agent 修改
↓
git diff
↓
Review
↓
Commit
```

---

# 📝 AI Collaboration Retrospective

請新增：

```text
RETROSPECTIVE.md
```

不需要寫長篇心得。

請回答：

1. 你用了哪些 AI / Agent？
2. AI 做得最好的一件事是什麼？
3. AI 搞砸的一件事是什麼？
4. 你怎麼發現它錯了？
5. 最後怎麼解決？
6. 如果重做一次，你會怎麼改變自己的 AI 協作方式？

---

## 必須保留一次 AI Failure

例如：

```md
## Incident

### 我想要什麼

點擊月餅一次，score +1。

### AI 做了什麼

AI 在兩個地方都更新 score，
導致一次點擊 +2。

### 我怎麼發現

測試失敗：

expected: 1
actual: 2

### 怎麼解決

我修改了 spec，
明確規定 score 只能由 updateScore() 修改，
再讓 AI 重新實作。
```

我們比較在意的不是：

> AI 有沒有犯錯？

而是：

> **你怎麼發現它犯錯，以及你怎麼修正你的開發流程。**

---

# Optional：後端

如果作品需要，可以加入：

* 排行榜
* 留言板
* Database
* API
* KV
* Serverless Function

例如：

* Cloudflare Workers
* D1
* KV
* Supabase
* Firebase

但後端不是必做。

不要為了看起來比較厲害硬加 backend。

---

# Repository 至少包含


```text
project/
├── README.md
├── SPEC.md
├── RETROSPECTIVE.md
├── src/
└── ...
```


---

# README 至少包含

```md
# Project Name

一句話介紹作品。

## Demo

https://...

## Development

如何安裝與執行。

## AI Tools

使用了哪些 AI / Coding Agent。
```


---

# 最後

這次不是：

> 「叫 AI 幫我做一個網站。」

而是：

> **「我能不能把一個模糊的想法，變成 AI 可以實作、我可以驗證，最後能真正交付的產品？」**

Coding Agent 很會寫 Code。

但需求、判斷與驗證，還是你的工作。

祝各位中秋快樂，然後記得把網站 deploy 出去。🌕

