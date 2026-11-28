extends RefCounted
class_name RecipeDB

const RECIPES := [
	{
		"id": "hp_potion",
		"name": "하급 체력 물약",
		"req_lv": 1,
		"xp": 25,
		"cost": {"slime_gel": 2},
	},
	{
		"id": "iron_dagger",
		"name": "수습생 단검",
		"req_lv": 1,
		"xp": 30,
		"cost": {"iron_ore": 2},
	},
	{
		"id": "wood_shield",
		"name": "참나무 방패",
		"req_lv": 1,
		"xp": 30,
		"cost": {"iron_ore": 1, "slime_gel": 1},
	},
	{
		"id": "rage_potion",
		"name": "광폭 영약",
		"req_lv": 2,
		"xp": 50,
		"cost": {"slime_gel": 2, "bat_wing": 2},
	},
	{
		"id": "crimson_blade",
		"name": "흑적 장검",
		"req_lv": 2,
		"xp": 70,
		"cost": {"iron_ore": 3, "bone_shard": 2},
	},
	{
		"id": "dragon_aegis",
		"name": "마력 방패",
		"req_lv": 3,
		"xp": 110,
		"cost": {"iron_ore": 3, "boss_core": 1},
	},
]
