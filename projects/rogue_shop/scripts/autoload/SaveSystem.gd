extends Node

const SAVE_PATH := "user://rogue_shop_save.json"

func save_game() -> void:
	var data := {
		"gold": GameState.gold,
		"day": GameState.day,
		"craft_level": GameState.craft_level,
		"shop_reputation": GameState.shop_reputation,
		"materials": GameState.materials,
		"inventory_goods": GameState.inventory_goods,
	}
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(data, "\t"))
		file.close()

func load_game() -> void:
	if not FileAccess.file_exists(SAVE_PATH):
		return
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if not file:
		return
	var parsed = JSON.parse_string(file.get_as_text())
	file.close()
	if typeof(parsed) == TYPE_DICTIONARY:
		GameState.gold = int(parsed.get("gold", GameState.gold))
		GameState.day = int(parsed.get("day", GameState.day))
		GameState.craft_level = int(parsed.get("craft_level", GameState.craft_level))
		GameState.shop_reputation = int(parsed.get("shop_reputation", GameState.shop_reputation))
