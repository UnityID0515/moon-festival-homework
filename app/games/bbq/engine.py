from typing import Optional, List, Dict, Any, Tuple


FOOD_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "beef": {
        "id": "beef",
        "name": "鮮嫩牛肉串",
        "icon": "🥩",
        "base_points": 100,
        "speed": 10.0,  # 10% per second
        "desc": "中秋烤肉靈魂！注意控制火候，雙面微焦香氣四溢。"
    },
    "tempura": {
        "id": "tempura",
        "name": "酥香甜不辣",
        "icon": "🍢",
        "base_points": 80,
        "speed": 15.0,  # 15% per second (cooks fast!)
        "desc": "熟成速度快，容易膨脹烤焦，需眼明手快及時翻面！"
    },
    "sausage": {
        "id": "sausage",
        "name": "特選黑豬香腸",
        "icon": "🌭",
        "base_points": 120,
        "speed": 8.0,   # 8% per second (slow & steady)
        "desc": "肉質扎實熟成較慢，慢火細烤最是多汁美味。"
    }
}


class Skewer:
    def __init__(self, food_id: str):
        food_meta = FOOD_DEFINITIONS.get(food_id, FOOD_DEFINITIONS["beef"])
        self.food_id: str = food_meta["id"]
        self.name: str = food_meta["name"]
        self.icon: str = food_meta["icon"]
        self.base_points: int = food_meta["base_points"]
        self.speed: float = food_meta["speed"]
        self.side_a: float = 0.0  # 0% - 100%+
        self.side_b: float = 0.0  # 0% - 100%+
        self.is_flipped: bool = False
        self.sauce_brushed: bool = False

    @property
    def status(self) -> str:
        """Evaluate doneness: burnt > perfect > half_done > raw"""
        if self.side_a > 100.0 or self.side_b > 100.0:
            return "burnt"
        if self.side_a >= 60.0 and self.side_b >= 60.0:
            return "perfect"
        if self.side_a >= 60.0 or self.side_b >= 60.0:
            return "half_done"
        return "raw"

    @property
    def status_label(self) -> str:
        s = self.status
        if s == "burnt":
            return "🔥 烤焦焦炭"
        if s == "perfect":
            return "✨ 完美熟成"
        if s == "half_done":
            return "⏳ 單面熟成"
        return "🌱 生肉微溫"

    @property
    def status_color(self) -> str:
        s = self.status
        if s == "burnt":
            return "text-red-400"
        if s == "perfect":
            return "text-amber-300"
        if s == "half_done":
            return "text-cyan-300"
        return "text-slate-400"

    def tick(self, dt: float = 1.0) -> None:
        """Cook the active side facing the fire."""
        gain = self.speed * dt
        if not self.is_flipped:
            self.side_a = min(120.0, self.side_a + gain)
        else:
            self.side_b = min(120.0, self.side_b + gain)


class BBQEngine:
    def __init__(self, num_slots: int = 3):
        self.slots: List[Optional[Skewer]] = [None] * num_slots
        self.score: int = 0
        self.served_count: int = 0
        self.last_message: str = "歡迎來到中秋露天烤肉！選擇下方食材放上烤網吧！"

    def place_food(self, slot_idx: int, food_id: str) -> Tuple[bool, str]:
        if slot_idx < 0 or slot_idx >= len(self.slots):
            return False, "無效的烤網位置"
        if self.slots[slot_idx] is not None:
            return False, "該烤位已有食材！"
        if food_id not in FOOD_DEFINITIONS:
            return False, "無效的食材種類"

        self.slots[slot_idx] = Skewer(food_id)
        name = FOOD_DEFINITIONS[food_id]["name"]
        self.last_message = f"將【{name}】放上了第 {slot_idx + 1} 號烤位！滋滋作響中～"
        return True, self.last_message

    def flip(self, slot_idx: int) -> Tuple[bool, str]:
        if slot_idx < 0 or slot_idx >= len(self.slots) or self.slots[slot_idx] is None:
            return False, "該烤位沒有食材可翻面！"
        skewer = self.slots[slot_idx]
        skewer.is_flipped = not skewer.is_flipped
        side_name = "反面 (Side B)" if skewer.is_flipped else "正面 (Side A)"
        self.last_message = f"為第 {slot_idx + 1} 號烤位的【{skewer.name}】翻面！現在換 {side_name} 受熱。"
        return True, self.last_message

    def brush_sauce(self, slot_idx: int) -> Tuple[bool, str]:
        if slot_idx < 0 or slot_idx >= len(self.slots) or self.slots[slot_idx] is None:
            return False, "該烤位沒有食材可刷醬！"
        skewer = self.slots[slot_idx]
        if skewer.sauce_brushed:
            return False, "已經刷過獨門烤肉醬囉！"
        skewer.sauce_brushed = True
        self.last_message = f"刷上特調濃郁中秋烤肉醬！美味度提升 1.5 倍！"
        return True, self.last_message

    def serve(self, slot_idx: int) -> Dict[str, Any]:
        if slot_idx < 0 or slot_idx >= len(self.slots) or self.slots[slot_idx] is None:
            return {"status": "empty", "points": 0, "message": "該烤位是空的！"}

        skewer = self.slots[slot_idx]
        status = skewer.status
        multiplier = 1.5 if skewer.sauce_brushed else 1.0

        if status == "perfect":
            points = int(skewer.base_points * multiplier)
            msg = f"太好吃了！【{skewer.name}】火候剛好，外酥內嫩！獲得 +{points} 分！"
        elif status == "burnt":
            points = 10
            msg = f"哎呀！【{skewer.name}】烤焦變木炭了... 勉強吃下一口，安慰獎 +10 分。"
        else:  # raw or half_done
            points = 0
            msg = f"等等！【{skewer.name}】裡面還是生的！吃了會肚子痛，獲得 0 分！"

        self.score += points
        if status == "perfect":
            self.served_count += 1

        self.slots[slot_idx] = None
        self.last_message = msg
        return {"status": status, "points": points, "message": msg}

    def tick(self, dt: float = 1.0) -> None:
        """Advance cooking progress for all occupied slots."""
        for skewer in self.slots:
            if skewer is not None:
                skewer.tick(dt)

    def reset(self) -> None:
        for i in range(len(self.slots)):
            self.slots[i] = None
        self.score = 0
        self.served_count = 0
        self.last_message = "烤爐已清空，準備開啟下一輪烤肉派對！"
