extends RefCounted
class_name ItemDB

const MATERIALS := {
	"slime_gel": {"name": "슬라임 점액", "color": Color(0.35, 0.9, 0.45)},
	"bat_wing": {"name": "박쥐 날개막", "color": Color(0.65, 0.45, 0.85)},
	"bone_shard": {"name": "마력 뼈조각", "color": Color(0.92, 0.90, 0.82)},
	"iron_ore": {"name": "던전 철광석", "color": Color(0.65, 0.72, 0.80)},
	"boss_core": {"name": "보스 마력핵", "color": Color(1.0, 0.45, 0.25)},
}

const GOODS := {
	"hp_potion": {"name": "하급 체력 물약", "price": 80, "type": "물약", "min_lv": 1, "desc": "용사 생존율 UP"},
	"iron_dagger": {"name": "수습생 단검", "price": 120, "type": "무기", "min_lv": 1, "desc": "가벼운 입문 단검"},
	"wood_shield": {"name": "참나무 방패", "price": 110, "type": "방패", "min_lv": 1, "desc": "기본 방어구"},
	"rage_potion": {"name": "광폭 영약", "price": 240, "type": "물약", "min_lv": 2, "desc": "공격력 증가 비약"},
	"crimson_blade": {"name": "흑적 장검", "price": 420, "type": "무기", "min_lv": 2, "desc": "은퇴 용사의 비기"},
	"dragon_aegis": {"name": "마력 방패", "price": 680, "type": "방패", "min_lv": 3, "desc": "보스전용 고급 방패"},
}
