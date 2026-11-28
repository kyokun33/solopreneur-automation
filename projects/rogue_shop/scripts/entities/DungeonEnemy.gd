extends Node2D
class_name DungeonEnemy

const PixelFxScript := preload("res://scripts/vfx/PixelFxPlayer.gd")

signal died(enemy: DungeonEnemy)

var enemy_id: String = "slime"
var enemy_name: String = "슬라임"
var max_hp: int = 50
var hp: int = 50
var atk: int = 10
var move_speed: float = 95.0
var is_boss: bool = false
var drop_mat: String = "slime_gel"
var base_price: int = 150
var gold_reward: int = 20

var sprite_vfx: AnimatedSprite2D
var hp_bg: ColorRect
var hp_fill: ColorRect
var capture_label: Label
var knockback_vel: Vector2 = Vector2.ZERO
var attack_cd: float = 0.0
var flash_timer: float = 0.0

func setup(kind: String, floor_num: int, boss_mode: bool = false) -> void:
	enemy_id = kind
	is_boss = boss_mode
	match kind:
		"slime":
			enemy_name = "독 슬라임"
			max_hp = 45 + floor_num * 12
			atk = 8 + floor_num * 2
			move_speed = 85.0
			drop_mat = "slime_gel"
			base_price = 140
			gold_reward = 18
		"bat":
			enemy_name = "동굴 박쥐"
			max_hp = 35 + floor_num * 10
			atk = 10 + floor_num * 2
			move_speed = 135.0
			drop_mat = "bat_wing"
			base_price = 180
			gold_reward = 24
		"flying-skull":
			enemy_name = "해골 마도사"
			max_hp = 65 + floor_num * 15
			atk = 14 + floor_num * 3
			move_speed = 105.0
			drop_mat = "bone_shard"
			base_price = 260
			gold_reward = 35
	if is_boss:
		enemy_name = ("중간보스: 거대 해골왕" if floor_num == 3 else "구역 보스: 심연의 마룡해골")
		max_hp = 220 + floor_num * 45
		atk = 18 + floor_num * 4
		move_speed = 115.0
		drop_mat = "boss_core"
		base_price = 520
		gold_reward = 150
	hp = max_hp

func _ready() -> void:
	sprite_vfx = AnimatedSprite2D.new()
	sprite_vfx.set_script(PixelFxScript)
	sprite_vfx.set("fx_name", enemy_id)
	var sc := 2.4 if is_boss else 1.5
	sprite_vfx.scale = Vector2(sc, sc)
	if is_boss:
		sprite_vfx.modulate = Color(1.0, 0.55, 0.55)
	add_child(sprite_vfx)

	hp_bg = ColorRect.new()
	hp_bg.size = Vector2(70 if is_boss else 46, 7)
	hp_bg.position = Vector2(-hp_bg.size.x * 0.5, -48 if is_boss else -34)
	hp_bg.color = Color(0.1, 0.1, 0.1, 0.85)
	add_child(hp_bg)

	hp_fill = ColorRect.new()
	hp_fill.size = hp_bg.size
	hp_fill.position = hp_bg.position
	hp_fill.color = Color(0.95, 0.25, 0.3) if is_boss else Color(0.3, 0.9, 0.4)
	add_child(hp_fill)

	capture_label = Label.new()
	capture_label.text = "[E] 포획가능!"
	capture_label.position = Vector2(-46, -68 if is_boss else -54)
	capture_label.add_theme_color_override("font_color", Color(1.0, 0.9, 0.2))
	capture_label.visible = false
	add_child(capture_label)

func _process(delta: float) -> void:
	if attack_cd > 0.0:
		attack_cd -= delta
	if flash_timer > 0.0:
		flash_timer -= delta
		if flash_timer <= 0.0:
			sprite_vfx.modulate = Color(1.0, 0.55, 0.55) if is_boss else Color.WHITE

	if knockback_vel.length() > 5.0:
		position += knockback_vel * delta
		knockback_vel = knockback_vel.lerp(Vector2.ZERO, 10.0 * delta)

	position.x = clampf(position.x, 120.0, 1160.0)
	position.y = clampf(position.y, 130.0, 620.0)

func step_ai(player_pos: Vector2, delta: float) -> int:
	var to_player := player_pos - position
	var dist := to_player.length()
	if dist > 36.0:
		position += to_player.normalized() * move_speed * delta
	if to_player.x != 0.0:
		sprite_vfx.flip_h = to_player.x < 0.0
	if dist < (55.0 if is_boss else 42.0) and attack_cd <= 0.0:
		attack_cd = 0.85
		return atk
	return 0

func take_damage(amount: int, from_pos: Vector2) -> void:
	hp = max(0, hp - amount)
	var ratio := float(hp) / float(max(1, max_hp))
	hp_fill.size.x = hp_bg.size.x * ratio
	knockback_vel = (position - from_pos).normalized() * (140.0 if is_boss else 240.0)
	sprite_vfx.modulate = Color(3.0, 3.0, 3.0, 1.0)
	flash_timer = 0.09
	capture_label.visible = can_capture()
	if hp <= 0:
		died.emit(self)

func can_capture() -> bool:
	return hp > 0 and float(hp) / float(max(1, max_hp)) <= 0.40
