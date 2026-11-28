extends Node

const SCENES := {
	"shop": "res://scenes/ShopScene.tscn",
	"workshop": "res://scenes/WorkshopScene.tscn",
	"dungeon": "res://scenes/DungeonScene.tscn",
}

@onready var container: Node = $SceneContainer
@onready var stats_label: Label = $HUD/TopBar/HBox/StatsLabel
@onready var btn_shop: Button = $HUD/TopBar/HBox/BtnShop
@onready var btn_workshop: Button = $HUD/TopBar/HBox/BtnWorkshop
@onready var btn_dungeon: Button = $HUD/TopBar/HBox/BtnDungeon

var current_scene: Node = null

func _ready() -> void:
	btn_shop.pressed.connect(func(): switch_scene("shop"))
	btn_workshop.pressed.connect(func(): switch_scene("workshop"))
	btn_dungeon.pressed.connect(func(): switch_scene("dungeon"))
	EventBus.scene_requested.connect(switch_scene)
	EventBus.gold_changed.connect(func(_v): _refresh_hud())
	EventBus.day_changed.connect(func(_v): _refresh_hud())
	EventBus.craft_skill_changed.connect(func(_lv, _xp): _refresh_hud())
	_refresh_hud()
	switch_scene("shop")

func switch_scene(scene_key: String) -> void:
	if not SCENES.has(scene_key):
		return
	if current_scene:
		current_scene.queue_free()
		current_scene = null
	var packed: PackedScene = load(SCENES[scene_key])
	if packed:
		current_scene = packed.instantiate()
		container.add_child(current_scene)

func _refresh_hud() -> void:
	stats_label.text = "Day %d  |  💰 %dG  |  제작 Lv.%d  |  평판 %d" % [
		GameState.day, GameState.gold, GameState.craft_level, GameState.shop_reputation
	]
