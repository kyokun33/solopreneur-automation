extends Node

var gold: int = 500
var day: int = 1
var craft_level: int = 1
var shop_reputation: int = 10
var current_floor: int = 1

var materials: Dictionary = {
	"슬라임 점액": 3,
	"녹슨 철조각": 2,
}

var inventory_goods: Dictionary = {
	"하급 체력 물약": 2,
	"수습생 단검": 1,
}

var captured_monsters: Array[Dictionary] = []
var companion_stock: Array[Dictionary] = []

func add_gold(amount: int) -> void:
	gold = max(0, gold + amount)
	EventBus.gold_changed.emit(gold)

func advance_day() -> void:
	day += 1
	EventBus.day_changed.emit(day)
	SaveSystem.save_game()
