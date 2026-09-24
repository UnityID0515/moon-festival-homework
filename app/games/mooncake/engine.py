import math
from typing import Dict, Any, Tuple


class Upgrade:
    def __init__(
        self,
        id: str,
        name: str,
        desc: str,
        icon: str,
        base_cost: int,
        cost_multiplier: float,
        upgrade_type: str,
        power: int,
        count: int = 0
    ):
        self.id = id
        self.name = name
        self.desc = desc
        self.icon = icon
        self.base_cost = base_cost
        self.cost_multiplier = cost_multiplier
        self.upgrade_type = upgrade_type  # 'cpc' or 'cps'
        self.power = power
        self.count = count

    @property
    def cost(self) -> int:
        return int(math.floor(self.base_cost * (self.cost_multiplier ** self.count)))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "icon": self.icon,
            "count": self.count,
            "cost": self.cost,
            "power": self.power,
            "type": self.upgrade_type
        }


class MooncakeEngine:
    def __init__(self):
        self.score: int = 0
        self.total_produced: int = 0
        self.fractional_progress: float = 0.0
        self.upgrades: Dict[str, Upgrade] = self._init_upgrades()
        self.achievements: Dict[str, Dict[str, Any]] = self._init_achievements()

    def _init_upgrades(self) -> Dict[str, Upgrade]:
        return {
            "mortar": Upgrade(
                id="mortar",
                name="玉兔搗藥杵",
                desc="玉兔隨身法寶，每次點擊產量 +1",
                icon="🐇",
                base_cost=15,
                cost_multiplier=1.15,
                upgrade_type="cpc",
                power=1
            ),
            "oven": Upgrade(
                id="oven",
                name="廣寒宮烤箱",
                desc="自動烘烤月餅，每秒自動產出 +1 顆",
                icon="🔥",
                base_cost=50,
                cost_multiplier=1.15,
                upgrade_type="cps",
                power=1
            ),
            "yolk": Upgrade(
                id="yolk",
                name="金沙鹹蛋黃",
                desc="金黃流沙蛋黃，每次點擊產量 +5",
                icon="🥚",
                base_cost=200,
                cost_multiplier=1.20,
                upgrade_type="cpc",
                power=5
            ),
            "blessing": Upgrade(
                id="blessing",
                name="嫦娥仙氣",
                desc="仙氣繚繞，每秒自動產出 +10 顆",
                icon="✨",
                base_cost=800,
                cost_multiplier=1.25,
                upgrade_type="cps",
                power=10
            ),
        }

    def _init_achievements(self) -> Dict[str, Dict[str, Any]]:
        return {
            "first_batch": {
                "id": "first_batch",
                "name": "初試身手",
                "desc": "累計烘烤 10 顆月餅",
                "icon": "🥮",
                "threshold": 10,
                "unlocked": False
            },
            "feast": {
                "id": "feast",
                "name": "中秋團圓",
                "desc": "累計烘烤 100 顆月餅",
                "icon": "🏮",
                "threshold": 100,
                "unlocked": False
            },
            "workshop": {
                "id": "workshop",
                "name": "廣寒作坊",
                "desc": "累計烘烤 1,000 顆月餅",
                "icon": "🏯",
                "threshold": 1000,
                "unlocked": False
            },
            "tycoon": {
                "id": "tycoon",
                "name": "月球烘焙大亨",
                "desc": "累計烘烤 10,000 顆月餅",
                "icon": "👑",
                "threshold": 10000,
                "unlocked": False
            }
        }

    @property
    def cpc(self) -> int:
        """Cakes Per Click."""
        bonus = sum(u.power * u.count for u in self.upgrades.values() if u.upgrade_type == "cpc")
        return 1 + bonus

    @property
    def cps(self) -> int:
        """Cakes Per Second."""
        return sum(u.power * u.count for u in self.upgrades.values() if u.upgrade_type == "cps")

    def click(self) -> int:
        gain = self.cpc
        self.score += gain
        self.total_produced += gain
        self._check_achievements()
        return gain

    def tick(self, dt: float = 1.0) -> int:
        if self.cps <= 0:
            return 0
        raw_gain = (self.cps * dt) + self.fractional_progress
        earned = int(raw_gain)
        self.fractional_progress = raw_gain - earned
        if earned > 0:
            self.score += earned
            self.total_produced += earned
            self._check_achievements()
        return earned

    def buy_upgrade(self, upgrade_id: str) -> Tuple[bool, str]:
        if upgrade_id not in self.upgrades:
            return False, "未知的升級項目"
        upgrade = self.upgrades[upgrade_id]
        if self.score < upgrade.cost:
            return False, f"月餅不足！需要 {upgrade.cost} 顆"
        self.score -= upgrade.cost
        upgrade.count += 1
        return True, f"成功購買 {upgrade.name}！"

    def _check_achievements(self) -> None:
        for ach in self.achievements.values():
            if not ach["unlocked"] and self.total_produced >= ach["threshold"]:
                ach["unlocked"] = True

    def reset(self) -> None:
        self.score = 0
        self.total_produced = 0
        self.fractional_progress = 0.0
        for u in self.upgrades.values():
            u.count = 0
        for a in self.achievements.values():
            a["unlocked"] = False
