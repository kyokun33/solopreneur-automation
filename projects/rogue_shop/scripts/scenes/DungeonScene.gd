extends Node2D

const PixelFxScript := preload("res://scripts/vfx/PixelFxPlayer.gd")
const MOVE_SPEED := 260.0

@onready var player: Node2D = $Player
@onready var player_sprite: Sprite2D = $Player/Sprite

var facing_right: bool = true
var attack_cooldown: float = 0.0

func _process(delta: float) -> void:
	var dir := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	if dir != Vector2.ZERO:
		player.position += dir * MOVE_SPEED * delta
		player.position.x = clampf(player.position.x, 160.0, 1120.0)
		player.position.y = clampf(player.position.y, 170.0, 590.0)
		if dir.x != 0.0:
			facing_right = dir.x > 0.0
			player_sprite.flip_h = not facing_right

	if attack_cooldown > 0.0:
		attack_cooldown -= delta

	if (Input.is_action_just_pressed("attack") or Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT)) and attack_cooldown <= 0.0:
		_spawn_slash()
		attack_cooldown = 0.35

func _spawn_slash() -> void:
	var vfx := AnimatedSprite2D.new()
	vfx.set_script(PixelFxScript)
	vfx.set("fx_name", "double-slash")
	vfx.set("free_on_finish", true)
	var offset_x := 65.0 if facing_right else -65.0
	vfx.position = player.position + Vector2(offset_x, -10.0)
	vfx.flip_h = not facing_right
	vfx.scale = Vector2(1.4, 1.4)
	add_child(vfx)
