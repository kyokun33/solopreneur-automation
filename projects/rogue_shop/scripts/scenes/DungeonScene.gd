extends Node2D

const Loader := preload("res://scripts/core/AssetLoader.gd")
const PixelFxScript := preload("res://scripts/vfx/PixelFxPlayer.gd")
const EnemyClass := preload("res://scripts/entities/DungeonEnemy.gd")

const MOVE_SPEED := 265.0
const MAX_FLOOR := 6

@onready var bg_sprite: Sprite2D = $BgSprite
@onready var entities: Node2D = $Entities
@onready var player: Node2D = $Entities/Player
@onready var floor_label: Label = $HUD/FloorPanel/VBox/FloorLabel
@onready var hp_label: Label = $HUD/FloorPanel/VBox/HpLabel
@onready var clear_overlay: PanelContainer = $HUD/ClearOverlay
@onready var clear_title: Label = $HUD/ClearOverlay/VBox/Title
@onready var clear_summary: Label = $HUD/ClearOverlay/VBox/Summary
@onready var btn_next: Button = $HUD/ClearOverlay/VBox/BtnNext
@onready var btn_gamble: Button = $HUD/ClearOverlay/VBox/BtnGamble
@onready var btn_return: Button = $HUD/ClearOverlay/VBox/BtnReturn

var player_sprite: Sprite2D
var current_floor: int = 1
var hp: int = 100
var max_hp: int = 100
var facing_right: bool = true
var attack_cd: float = 0.0
var dash_cd: float = 0.0
var hitstop_timer: float = 0.0
var shake_timer: float = 0.0
var walk_time: float = 0.0
var enemies: Array = []
var floor_cleared: bool = false
var run_gold: int = 0
var portal_vfx: AnimatedSprite2D = null

func _ready() -> void:
	bg_sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	bg_sprite.texture = Loader.load_tex("res://assets/bg/dungeon_bg.png")

	var sh := ColorRect.new()
	sh.size = Vector2(46, 14)
	sh.position = Vector2(-23, 34)
	sh.color = Color(0, 0, 0, 0.5)
	player.add_child(sh)

	player_sprite = Sprite2D.new()
	player_sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	player_sprite.texture = Loader.load_tex("res://assets/sprites/hero_idle.png")
	player_sprite.scale = Vector2(0.42, 0.42)
	player.add_child(player_sprite)

	# 4 corner dungeon torches
	for pos in [Vector2(190, 95), Vector2(1090, 95), Vector2(90, 520), Vector2(1190, 520)]:
		var t := AnimatedSprite2D.new()
		t.set_script(PixelFxScript)
		t.set("fx_name", "torch")
		t.position = pos
		t.scale = Vector2(1.1, 1.1)
		add_child(t)

	max_hp = GameState.hero_max_hp
	hp = max_hp
	btn_next.pressed.connect(_on_next_floor)
	btn_gamble.pressed.connect(_on_gamble_altar)
	btn_return.pressed.connect(func():
		GameState.add_gold(run_gold)
		EventBus.scene_requested.emit("shop")
	)
	_start_floor(1)

func _start_floor(floor_num: int) -> void:
	current_floor = floor_num
	floor_cleared = false
	clear_overlay.visible = false
	if portal_vfx and is_instance_valid(portal_vfx):
		portal_vfx.queue_free()
		portal_vfx = null
	for e in enemies:
		if is_instance_valid(e):
			e.queue_free()
	enemies.clear()

	player.position = Vector2(640, 480)
	var tag := "일반 구역"
	if floor_num == 3:
		tag = "⚠️ 중간보스전!"
	elif floor_num == MAX_FLOOR:
		tag = "🔥 구역 최종 보스전!"
	floor_label.text = "🗡️ 무한 던전 Stage %d / %d (%s)" % [floor_num, MAX_FLOOR, tag]
	_update_hp_ui()

	if floor_num == 3 or floor_num == MAX_FLOOR:
		_spawn_enemy("flying-skull", Vector2(640, 220), true)
		_spawn_enemy("slime", Vector2(390, 270), false)
		_spawn_enemy("bat", Vector2(890, 270), false)
	else:
		var count := 3 + floor_num
		var pool := ["slime", "bat", "flying-skull"]
		for i in range(count):
			var kind: String = pool[i % (2 if floor_num < 3 else 3)]
			var pos := Vector2(randf_range(220.0, 1060.0), randf_range(160.0, 340.0))
			_spawn_enemy(kind, pos, false)

func _spawn_enemy(kind: String, pos: Vector2, is_boss: bool) -> void:
	var e := EnemyClass.new()
	e.setup(kind, current_floor, is_boss)
	e.position = pos
	e.died.connect(_on_enemy_died)
	entities.add_child(e)
	enemies.append(e)

func _process(delta: float) -> void:
	if shake_timer > 0.0:
		shake_timer -= delta
		position = Vector2(randf_range(-5.0, 5.0), randf_range(-5.0, 5.0))
	else:
		position = Vector2.ZERO

	if hitstop_timer > 0.0:
		hitstop_timer -= delta
		return

	if floor_cleared:
		return

	if attack_cd > 0.0:
		attack_cd -= delta
	if dash_cd > 0.0:
		dash_cd -= delta

	var dir := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	if dir != Vector2.ZERO:
		var spd := MOVE_SPEED
		if Input.is_key_pressed(KEY_SHIFT) and dash_cd <= 0.0:
			spd = MOVE_SPEED * 3.0
			dash_cd = GameState.hero_dash_cd
			_spawn_vfx("collect-burst", player.position, 0.8)
		player.position += dir * spd * delta
		player.position.x = clampf(player.position.x, 120.0, 1160.0)
		player.position.y = clampf(player.position.y, 130.0, 600.0)
		walk_time += delta * 15.0
		player_sprite.position.y = -absf(sin(walk_time)) * 6.0
		if dir.x != 0.0:
			facing_right = dir.x > 0.0
			player_sprite.flip_h = not facing_right
	else:
		player_sprite.position.y = lerpf(player_sprite.position.y, 0.0, 12.0 * delta)

	if (Input.is_action_just_pressed("attack") or Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT)) and attack_cd <= 0.0:
		_do_attack()
		attack_cd = 0.34

	if Input.is_key_pressed(KEY_E):
		_try_capture()

	for e in enemies:
		if not is_instance_valid(e):
			continue
		var dmg: int = e.step_ai(player.position, delta)
		if dmg > 0:
			_take_player_damage(dmg)

func _do_attack() -> void:
	SfxManager.play_slash()
	var slash_dir := 1.0 if facing_right else -1.0
	var slash_pos := player.position + Vector2(62.0 * slash_dir, -8.0)
	var vfx := _spawn_vfx("double-slash", slash_pos, 1.35)
	vfx.flip_h = not facing_right

	var hit_any := false
	for e in enemies.duplicate():
		if not is_instance_valid(e):
			continue
		if e.position.distance_to(slash_pos) <= (125.0 if e.is_boss else 105.0):
			var dmg := GameState.hero_atk + randi_range(-3, 6)
			e.take_damage(dmg, player.position)
			_spawn_floating_text("-%d" % dmg, e.position + Vector2(0, -35), Color(1.0, 0.85, 0.2))
			hit_any = true
	if hit_any:
		SfxManager.play_hit()
		hitstop_timer = 0.045
		shake_timer = 0.12

func _try_capture() -> void:
	for e in enemies.duplicate():
		if not is_instance_valid(e):
			continue
		if e.can_capture() and e.position.distance_to(player.position) <= 130.0:
			SfxManager.play_capture()
			_spawn_vfx("magic-circle-cast", e.position, 1.4)
			GameState.captured_monsters.append({
				"id": e.enemy_id,
				"name": e.enemy_name,
				"base_price": e.base_price,
			})
			_spawn_floating_text("포획 성공! (%s)" % e.enemy_name, e.position + Vector2(-40, -50), Color(0.4, 1.0, 0.9))
			enemies.erase(e)
			e.queue_free()
			_check_floor_clear()
			return

func _on_enemy_died(e) -> void:
	_spawn_vfx("small-explosion", e.position, 1.2 if e.is_boss else 0.8)
	_spawn_vfx("collect-burst", e.position, 1.0)
	SfxManager.play_coin()
	run_gold += e.gold_reward
	GameState.add_material(e.drop_mat, 2 if e.is_boss else 1)
	if randf() < 0.45:
		GameState.add_material("iron_ore", 1)
	_spawn_floating_text("+%dG  재료획득!" % e.gold_reward, e.position + Vector2(-30, -30), Color(0.5, 1.0, 0.5))
	enemies.erase(e)
	e.queue_free()
	_check_floor_clear()

func _check_floor_clear() -> void:
	if enemies.is_empty() and not floor_cleared:
		floor_cleared = true
		portal_vfx = _spawn_vfx("portal", Vector2(640, 175), 1.6)
		clear_overlay.visible = true
		btn_gamble.visible = (current_floor == 3 or current_floor == 5)
		btn_gamble.disabled = false
		if current_floor >= MAX_FLOOR:
			clear_title.text = "🏆 구역 최종 보스 격파 완료!"
			clear_summary.text = "이번 탐험 획득 골드: +%dG | 포획 몬스터: %d마리" % [run_gold, GameState.captured_monsters.size()]
			btn_next.visible = false
		else:
			clear_title.text = "✨ Stage %d 클리어!" % current_floor
			clear_summary.text = "획득 골드: +%dG | 계속 내려갈지, 상점으로 돌아갈지 선택하세요!" % run_gold
			btn_next.visible = true

func _on_next_floor() -> void:
	_start_floor(current_floor + 1)

func _on_gamble_altar() -> void:
	btn_gamble.disabled = true
	if randf() < 0.55:
		run_gold *= 2
		SfxManager.play_levelup()
		clear_summary.text = "🎲 대성공!! 이번 탐험 골드 2배 -> +%dG!" % run_gold
	else:
		run_gold = int(run_gold * 0.5)
		SfxManager.play_hit()
		clear_summary.text = "💀 꽝! 골드가 절반으로 줄었습니다 -> +%dG" % run_gold

func _take_player_damage(amount: int) -> void:
	hp = max(0, hp - amount)
	_update_hp_ui()
	_spawn_floating_text("-%d" % amount, player.position + Vector2(0, -40), Color(1.0, 0.25, 0.25))
	shake_timer = 0.1
	if hp <= 0:
		GameState.add_gold(int(run_gold * 0.5))
		EventBus.log_message.emit("체력 고갈로 상점으로 긴급 귀환했습니다 (+%dG)" % int(run_gold * 0.5))
		EventBus.scene_requested.emit("shop")

func _update_hp_ui() -> void:
	hp_label.text = "❤️ HP: %d / %d  |  ⚔️ ATK: %d  |  탐험골드: +%dG" % [hp, max_hp, GameState.hero_atk, run_gold]

func _spawn_vfx(fx_name: String, pos: Vector2, sc: float) -> AnimatedSprite2D:
	var vfx := AnimatedSprite2D.new()
	vfx.set_script(PixelFxScript)
	vfx.set("fx_name", fx_name)
	vfx.set("free_on_finish", true)
	vfx.position = pos
	vfx.scale = Vector2(sc, sc)
	entities.add_child(vfx)
	return vfx

func _spawn_floating_text(txt: String, pos: Vector2, col: Color) -> void:
	var lbl := Label.new()
	lbl.text = txt
	lbl.position = pos
	lbl.add_theme_color_override("font_color", col)
	entities.add_child(lbl)
	var tw := create_tween()
	tw.tween_property(lbl, "position:y", pos.y - 28.0, 0.55)
	tw.parallel().tween_property(lbl, "modulate:a", 0.0, 0.55)
	tw.tween_callback(lbl.queue_free)
