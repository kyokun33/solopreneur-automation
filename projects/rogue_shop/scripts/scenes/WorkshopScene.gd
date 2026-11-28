extends Node2D

const Loader := preload("res://scripts/core/AssetLoader.gd")
const PixelFxScript := preload("res://scripts/vfx/PixelFxPlayer.gd")
const ItemDBScript := preload("res://scripts/data/ItemDB.gd")
const RecipeDBScript := preload("res://scripts/data/RecipeDB.gd")

@onready var bg_sprite: Sprite2D = $BgSprite
@onready var world: Node2D = $World
@onready var mat_label: Label = $HUD/BottomBar/LeftPanel/VBox/MatLabel
@onready var recipe_list: VBoxContainer = $HUD/BottomBar/LeftPanel/VBox/RecipeList
@onready var monster_list: VBoxContainer = $HUD/BottomBar/RightPanel/VBox/MonsterList
@onready var status_label: Label = $HUD/BottomBar/RightPanel/VBox/StatusLabel

func _ready() -> void:
	bg_sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	bg_sprite.texture = Loader.load_tex("res://assets/bg/workshop_bg.png")

	var fire := AnimatedSprite2D.new()
	fire.set_script(PixelFxScript)
	fire.set("fx_name", "campfire")
	fire.position = Vector2(145, 290)
	fire.scale = Vector2(1.4, 1.4)
	world.add_child(fire)

	EventBus.inventory_changed.connect(_refresh_all)
	EventBus.craft_skill_changed.connect(func(_lv, _xp): _refresh_all())
	_refresh_all()

func _refresh_all() -> void:
	var m := GameState.materials
	mat_label.text = "점액 %d | 날개 %d | 뼈 %d | 철광석 %d | 보스핵 %d (제작 Lv.%d, XP %d/%d)" % [
		int(m.get("slime_gel", 0)), int(m.get("bat_wing", 0)), int(m.get("bone_shard", 0)),
		int(m.get("iron_ore", 0)), int(m.get("boss_core", 0)),
		GameState.craft_level, GameState.craft_xp, GameState.craft_level * 80
	]

	for c in recipe_list.get_children():
		c.queue_free()
	for r in RecipeDBScript.RECIPES:
		var btn := Button.new()
		var good_info: Dictionary = ItemDBScript.GOODS.get(r["id"], {})
		var cost_txt := ""
		for k in r["cost"].keys():
			cost_txt += "%s×%d " % [ItemDBScript.MATERIALS[k]["name"], int(r["cost"][k])]
		var locked := GameState.craft_level < int(r["req_lv"])
		if locked:
			btn.text = "🔒 [Lv.%d] %s (%dG)" % [r["req_lv"], r["name"], int(good_info.get("price", 0))]
			btn.disabled = true
		else:
			btn.text = "⚒️ %s (%s) -> %dG [보유:%d]" % [
				r["name"], cost_txt.strip_edges(), int(good_info.get("price", 0)),
				int(GameState.inventory_goods.get(r["id"], 0))
			]
			btn.disabled = not GameState.can_craft(r)
			btn.pressed.connect(func():
				if GameState.craft_item(r):
					SfxManager.play_coin()
					status_label.text = "✅ '%s' 제작 완료! 상점 진열대에 올리세요." % r["name"]
			)
		recipe_list.add_child(btn)

	for c in monster_list.get_children():
		c.queue_free()
	# Show captured monsters visually in the taming pens!
	for child in world.get_children():
		if child.has_meta("pen_mon"):
			child.queue_free()

	if GameState.captured_monsters.is_empty():
		var empty_lbl := Label.new()
		empty_lbl.text = "포획한 몬스터가 없습니다. (던전에서 E키로 생포)"
		monster_list.add_child(empty_lbl)
	else:
		for i in range(GameState.captured_monsters.size()):
			var mon: Dictionary = GameState.captured_monsters[i]
			if i < 4:
				var pen_spr := AnimatedSprite2D.new()
				pen_spr.set_script(PixelFxScript)
				pen_spr.set("fx_name", str(mon.get("id", "slime")))
				pen_spr.set_meta("pen_mon", true)
				pen_spr.position = Vector2(770 + i * 110, 275)
				pen_spr.scale = Vector2(1.5, 1.5)
				world.add_child(pen_spr)
			var btn := Button.new()
			btn.text = "🐾 '%s' 동료 훈련 (기본 %dG / 변이 시 3배!)" % [mon["name"], int(mon["base_price"])]
			var idx := i
			btn.pressed.connect(func():
				var comp := GameState.train_captured_monster(idx)
				if not comp.is_empty():
					if comp["mutant"]:
						SfxManager.play_levelup()
						status_label.text = "🌟 대박!! '%s' 변이 각성! (%dG 판매)" % [comp["name"], comp["price"]]
					else:
						SfxManager.play_capture()
						status_label.text = "✅ '%s' 훈련 완료! (%dG)" % [comp["name"], comp["price"]]
			)
			monster_list.add_child(btn)
