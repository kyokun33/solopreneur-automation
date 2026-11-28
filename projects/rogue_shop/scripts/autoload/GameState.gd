extends Node

var gold: int = 300
var day: int = 1
var craft_level: int = 1
var craft_xp: int = 0
var shop_reputation: int = 10

# Hero combat stats (upgradable with gold!)
var hero_max_hp: int = 100
var hero_atk: int = 22
var hero_dash_cd: float = 0.7

# Materials farmed in dungeon
var materials: Dictionary = {
	"slime_gel": 3,
	"bat_wing": 0,
	"bone_shard": 0,
	"iron_ore": 2,
	"boss_core": 0,
}

# Crafted goods ready to display/sell
var inventory_goods: Dictionary = {
	"hp_potion": 2,
	"iron_dagger": 1,
}

# Shop display slots (max 4 slots) -> item dicts: {"kind": "good"|"companion", "id": ..., "name": ..., "price": ..., "mutant": bool}
var shop_shelf: Array[Dictionary] = [
	{"kind": "good", "id": "hp_potion", "name": "하급 체력 물약", "price": 80, "mutant": false},
	{"kind": "good", "id": "iron_dagger", "name": "수습생 단검", "price": 120, "mutant": false},
]

# Captured monsters waiting to be trained into companions
var captured_monsters: Array[Dictionary] = []
# Trained companion monsters ready to sell in shop
var companion_stock: Array[Dictionary] = []

func add_gold(amount: int) -> void:
	gold = max(0, gold + amount)
	EventBus.gold_changed.emit(gold)

func add_material(mat_id: String, count: int = 1) -> void:
	materials[mat_id] = int(materials.get(mat_id, 0)) + count
	EventBus.inventory_changed.emit()

func add_craft_xp(xp: int) -> void:
	craft_xp += xp
	var next_req := craft_level * 80
	while craft_xp >= next_req:
		craft_xp -= next_req
		craft_level += 1
		next_req = craft_level * 80
		SfxManager.play_levelup()
		EventBus.log_message.emit("🎉 제작 숙련도 Lv.%d 달성! 신규 레시피 해금!" % craft_level)
	EventBus.craft_skill_changed.emit(craft_level, craft_xp)

func can_craft(recipe: Dictionary) -> bool:
	if craft_level < int(recipe.get("req_lv", 1)):
		return false
	var cost: Dictionary = recipe.get("cost", {})
	for k in cost.keys():
		if int(materials.get(k, 0)) < int(cost[k]):
			return false
	return true

func craft_item(recipe: Dictionary) -> bool:
	if not can_craft(recipe):
		return false
	var cost: Dictionary = recipe.get("cost", {})
	for k in cost.keys():
		materials[k] = int(materials.get(k, 0)) - int(cost[k])
	var gid: String = recipe["id"]
	inventory_goods[gid] = int(inventory_goods.get(gid, 0)) + 1
	add_craft_xp(int(recipe.get("xp", 25)))
	EventBus.inventory_changed.emit()
	return true

func train_captured_monster(index: int) -> Dictionary:
	if index < 0 or index >= captured_monsters.size():
		return {}
	var mon: Dictionary = captured_monsters[index]
	captured_monsters.remove_at(index)
	# 25% chance of shiny/mutant evolution!
	var is_mutant: bool = randf() < 0.25
	var base_price: int = int(mon.get("base_price", 150))
	var final_price: int = base_price * (3 if is_mutant else 1)
	var mon_name: String = str(mon.get("name", "몬스터"))
	var title: String = ("★변이 황금 " + mon_name) if is_mutant else ("훈련된 동료 " + mon_name)
	var comp: Dictionary = {
		"kind": "companion",
		"id": str(mon.get("id", "slime")),
		"name": title,
		"price": final_price,
		"mutant": is_mutant,
	}
	companion_stock.append(comp)
	EventBus.inventory_changed.emit()
	return comp

func advance_day() -> void:
	day += 1
	EventBus.day_changed.emit(day)
	SaveSystem.save_game()
