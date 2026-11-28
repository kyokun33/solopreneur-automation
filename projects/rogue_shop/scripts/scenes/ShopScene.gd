extends Node2D

const Loader := preload("res://scripts/core/AssetLoader.gd")
const PixelFxScript := preload("res://scripts/vfx/PixelFxPlayer.gd")
const HeroAnimScript := preload("res://scripts/entities/HeroAnimator.gd")
const AmbientScript := preload("res://scripts/vfx/AmbientWorldFX.gd")
const ItemDBScript := preload("res://scripts/data/ItemDB.gd")

@onready var bg_sprite: Sprite2D = $BgSprite
@onready var world: Node2D = $World
@onready var hero_node: Node2D = $World/Hero
@onready var customers_node: Node2D = $World/Customers
@onready var shelf_list: VBoxContainer = $HUD/BottomBar/ShelfPanel/VBox/ShelfList
@onready var stock_list: VBoxContainer = $HUD/BottomBar/StockPanel/VBox/StockList
@onready var btn_open: Button = $HUD/BottomBar/ActionPanel/VBox/BtnOpenShop
@onready var btn_atk: Button = $HUD/BottomBar/ActionPanel/VBox/HBoxUp/BtnUpgradeAtk
@onready var btn_hp: Button = $HUD/BottomBar/ActionPanel/VBox/HBoxUp/BtnUpgradeHp
@onready var log_label: Label = $HUD/BottomBar/ActionPanel/VBox/LogLabel

var hero_anim: AnimatedSprite2D
var shop_busy: bool = false

func _ready() -> void:
	bg_sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	bg_sprite.texture = Loader.load_tex("res://assets/bg/shop_bg.png")
	bg_sprite.scale = Vector2(1.03, 1.03)

	var ambient := Node2D.new()
	ambient.set_script(AmbientScript)
	ambient.setup("shop")
	add_child(ambient)

	# Hero shadow + 8-dir SD animator (proportioned to 2D shop tiles!)
	var shadow := ColorRect.new()
	shadow.size = Vector2(52, 14)
	shadow.position = Vector2(-26, -6)
	shadow.color = Color(0, 0, 0, 0.45)
	hero_node.add_child(shadow)

	hero_anim = AnimatedSprite2D.new()
	hero_anim.set_script(HeroAnimScript)
	hero_anim.scale = Vector2(0.88, 0.88)
	hero_node.add_child(hero_anim)

	# Ambient torches in shop
	for pos in [Vector2(445, 130), Vector2(730, 130), Vector2(1165, 145)]:
		var t := AnimatedSprite2D.new()
		t.set_script(PixelFxScript)
		t.set("fx_name", "torch")
		t.position = pos
		t.scale = Vector2(0.95, 0.95)
		world.add_child(t)

	btn_open.pressed.connect(_start_shop_wave)
	btn_atk.pressed.connect(func():
		if GameState.gold >= 150:
			GameState.add_gold(-150)
			GameState.hero_atk += 5
			SfxManager.play_levelup()
			log_label.text = "⚔️ 주인공 공격력 상승! (현재 ATK: %d)" % GameState.hero_atk
		else:
			log_label.text = "골드가 부족합니다! (필요: 150G)"
	)
	btn_hp.pressed.connect(func():
		if GameState.gold >= 120:
			GameState.add_gold(-120)
			GameState.hero_max_hp += 25
			SfxManager.play_levelup()
			log_label.text = "❤️ 주인공 최대체력 상승! (현재 HP: %d)" % GameState.hero_max_hp
		else:
			log_label.text = "골드가 부족합니다! (필요: 120G)"
	)
	EventBus.inventory_changed.connect(_refresh_ui)
	_refresh_ui()

func _process(delta: float) -> void:
	var dir := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	if dir != Vector2.ZERO:
		hero_node.position += dir * 215.0 * delta
		hero_node.position.x = clampf(hero_node.position.x, 180.0, 1130.0)
		hero_node.position.y = clampf(hero_node.position.y, 260.0, 485.0)
		if hero_node.position.x > 1060.0 and hero_node.position.y > 435.0:
			EventBus.scene_requested.emit("dungeon")
	hero_anim.update_move(dir)
	# Subtle Dave-the-Diver parallax background shift!
	var offset_from_center := (hero_node.position - Vector2(640, 360)) * -0.025
	bg_sprite.position = Vector2(640, 360) + offset_from_center

func _refresh_ui() -> void:
	for c in shelf_list.get_children():
		c.queue_free()
	if GameState.shop_shelf.is_empty():
		var lbl := Label.new()
		lbl.text = "진열대가 비었습니다!"
		shelf_list.add_child(lbl)
	else:
		for item in GameState.shop_shelf:
			var lbl := Label.new()
			lbl.text = "• %s (%dG)" % [item["name"], int(item["price"])]
			if item.get("mutant", false):
				lbl.add_theme_color_override("font_color", Color(1.0, 0.88, 0.25))
			shelf_list.add_child(lbl)

	for c in stock_list.get_children():
		c.queue_free()
	for gid in GameState.inventory_goods.keys():
		var cnt := int(GameState.inventory_goods[gid])
		if cnt <= 0:
			continue
		var info: Dictionary = ItemDBScript.GOODS.get(gid, {})
		var btn := Button.new()
		btn.text = "+ %s (%dG) [%d]" % [info.get("name", gid), int(info.get("price", 50)), cnt]
		btn.disabled = GameState.shop_shelf.size() >= 4
		var item_id: String = gid
		btn.pressed.connect(func():
			if GameState.shop_shelf.size() < 4 and int(GameState.inventory_goods.get(item_id, 0)) > 0:
				GameState.inventory_goods[item_id] -= 1
				GameState.shop_shelf.append({
					"kind": "good",
					"id": item_id,
					"name": info["name"],
					"price": info["price"],
					"mutant": false,
				})
				_refresh_ui()
		)
		stock_list.add_child(btn)

	for i in range(GameState.companion_stock.size()):
		var comp: Dictionary = GameState.companion_stock[i]
		var btn := Button.new()
		btn.text = "+ 🐾 %s (%dG)" % [comp["name"], int(comp["price"])]
		btn.disabled = GameState.shop_shelf.size() >= 4
		var idx := i
		btn.pressed.connect(func():
			if GameState.shop_shelf.size() < 4 and idx < GameState.companion_stock.size():
				var picked: Dictionary = GameState.companion_stock[idx]
				GameState.companion_stock.remove_at(idx)
				GameState.shop_shelf.append(picked)
				_refresh_ui()
		)
		stock_list.add_child(btn)

func _start_shop_wave() -> void:
	if shop_busy:
		return
	if GameState.shop_shelf.is_empty():
		log_label.text = "⚠️ 진열대에 물건을 올려주세요!"
		return
	shop_busy = true
	btn_open.disabled = true
	log_label.text = "🔔 용사 손님들이 던전 도전 전 물건을 사러 옵니다!"

	var specs := [
		{"name": "초보 검사 카일", "tint": Color.WHITE, "x": 450.0},
		{"name": "견습 기사 리나", "tint": Color(1.0, 0.78, 0.88), "x": 640.0},
		{"name": "베테랑 레온", "tint": Color(0.8, 1.0, 0.82), "x": 830.0},
	]
	for sp in specs:
		await get_tree().create_timer(0.45).timeout
		_spawn_hero_customer(sp["name"], sp["tint"], sp["x"])

	await get_tree().create_timer(2.4).timeout
	GameState.advance_day()
	shop_busy = false
	btn_open.disabled = false

func _spawn_hero_customer(h_name: String, tint: Color, target_x: float) -> void:
	var npc := Node2D.new()
	npc.position = Vector2(540, 485)
	customers_node.add_child(npc)

	var sh := ColorRect.new()
	sh.size = Vector2(44, 12)
	sh.position = Vector2(-22, -6)
	sh.color = Color(0, 0, 0, 0.4)
	npc.add_child(sh)

	var spr := Sprite2D.new()
	spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	spr.texture = Loader.load_tex("res://assets/sprites/customer_knight.png")
	spr.scale = Vector2(0.46, 0.46)
	spr.position = Vector2(0, -40)
	spr.modulate = tint
	npc.add_child(spr)

	var tag := Label.new()
	tag.text = h_name
	tag.position = Vector2(-46, -98)
	npc.add_child(tag)

	var tw := create_tween()
	tw.tween_property(npc, "position", Vector2(target_x, 360.0), 0.75)
	tw.tween_callback(func():
		if not GameState.shop_shelf.is_empty():
			var sold: Dictionary = GameState.shop_shelf.pop_front()
			var earned := int(sold["price"])
			GameState.add_gold(earned)
			GameState.shop_reputation += 1
			SfxManager.play_coin()
			var fx := AnimatedSprite2D.new()
			fx.set_script(PixelFxScript)
			fx.set("fx_name", "coin-spin")
			fx.position = npc.position + Vector2(0, -85)
			customers_node.add_child(fx)
			get_tree().create_timer(0.75).timeout.connect(fx.queue_free)
			log_label.text = "💰 %s님이 '%s' 구매! (+%dG)" % [h_name, sold["name"], earned]
			_refresh_ui()
		else:
			log_label.text = "%s: \"물건이 다 팔렸네요!\"" % h_name
	)
	tw.tween_interval(0.65)
	tw.tween_property(npc, "position", Vector2(1110.0, 460.0), 0.85)
	tw.tween_callback(npc.queue_free)
