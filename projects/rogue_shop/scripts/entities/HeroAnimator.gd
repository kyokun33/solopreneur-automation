extends AnimatedSprite2D
class_name HeroAnimator

const Loader := preload("res://scripts/core/AssetLoader.gd")

var current_dir_col: int = 0 # 0=down, 1=down-right, 2=right, 3=up-right, 4=up
var is_flipped: bool = false
var is_attacking: bool = false

func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	offset = Vector2(0, -48)
	_build_animations()
	play("idle_0")

func _build_animations() -> void:
	var walk_tex := Loader.load_tex("res://assets/sprites/hero_sd_walk.png")
	var atk_tex := Loader.load_tex("res://assets/sprites/hero_sd_attack.png")
	var sf := SpriteFrames.new()

	for col in range(5):
		var idle_name := "idle_%d" % col
		sf.add_animation(idle_name)
		sf.set_animation_speed(idle_name, 4.0)
		sf.set_animation_loop(idle_name, true)
		var f0 := AtlasTexture.new()
		f0.atlas = walk_tex
		f0.region = Rect2(col * 128, 0, 128, 128)
		sf.add_frame(idle_name, f0)

		var walk_name := "walk_%d" % col
		sf.add_animation(walk_name)
		sf.set_animation_speed(walk_name, 8.0)
		sf.set_animation_loop(walk_name, true)
		for row in range(2):
			var wf := AtlasTexture.new()
			wf.atlas = walk_tex
			wf.region = Rect2(col * 128, row * 128, 128, 128)
			sf.add_frame(walk_name, wf)

		var atk_name := "attack_%d" % col
		sf.add_animation(atk_name)
		sf.set_animation_speed(atk_name, 14.0)
		sf.set_animation_loop(atk_name, false)
		for row in range(2):
			var af := AtlasTexture.new()
			af.atlas = atk_tex
			af.region = Rect2(col * 128, row * 128, 128, 128)
			sf.add_frame(atk_name, af)

	sprite_frames = sf
	animation_finished.connect(_on_anim_finished)

func set_direction_from_vector(dir: Vector2) -> void:
	if dir.length_squared() < 0.01:
		return
	var ang := rad_to_deg(dir.angle()) # 0=right, 90=down, -90=up, 180/-180=left
	if ang >= 67.5 and ang < 112.5:
		current_dir_col = 0; is_flipped = false # Down
	elif ang >= 22.5 and ang < 67.5:
		current_dir_col = 1; is_flipped = false # Down-Right
	elif ang >= 112.5 and ang < 157.5:
		current_dir_col = 1; is_flipped = true  # Down-Left
	elif ang >= -22.5 and ang < 22.5:
		current_dir_col = 2; is_flipped = false # Right
	elif ang >= 157.5 or ang < -157.5:
		current_dir_col = 2; is_flipped = true  # Left
	elif ang >= -67.5 and ang < -22.5:
		current_dir_col = 3; is_flipped = false # Up-Right
	elif ang >= -157.5 and ang < -112.5:
		current_dir_col = 3; is_flipped = true  # Up-Left
	else:
		current_dir_col = 4; is_flipped = false # Up
	flip_h = is_flipped

func update_move(dir: Vector2) -> void:
	if is_attacking:
		return
	if dir.length_squared() > 0.01:
		set_direction_from_vector(dir)
		var anim := "walk_%d" % current_dir_col
		if animation != anim or not is_playing():
			play(anim)
	else:
		var anim := "idle_%d" % current_dir_col
		if animation != anim:
			play(anim)

func play_attack(dir: Vector2 = Vector2.ZERO) -> void:
	if dir.length_squared() > 0.01:
		set_direction_from_vector(dir)
	is_attacking = true
	play("attack_%d" % current_dir_col)

func _on_anim_finished() -> void:
	if is_attacking:
		is_attacking = false
		play("idle_%d" % current_dir_col)
