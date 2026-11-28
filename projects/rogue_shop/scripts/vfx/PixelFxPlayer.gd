extends AnimatedSprite2D
class_name PixelFxPlayer

const Loader := preload("res://scripts/core/AssetLoader.gd")

@export var fx_name: String = "torch"
@export var auto_play: bool = true
@export var free_on_finish: bool = false

func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	if fx_name != "":
		load_pixelfx(fx_name)
		if auto_play:
			play("default")

func load_pixelfx(name_id: String) -> bool:
	var png_path := "res://assets/vfx/%s.png" % name_id
	var json_path := "res://assets/vfx/%s.json" % name_id
	var tex := Loader.load_tex(png_path)
	if tex == null:
		push_warning("PixelFx texture missing: " + png_path)
		return false

	var abs_json := ProjectSettings.globalize_path(json_path)
	if not FileAccess.file_exists(abs_json):
		push_warning("PixelFx json missing: " + json_path)
		return false

	var file := FileAccess.open(abs_json, FileAccess.READ)
	var data = JSON.parse_string(file.get_as_text())
	file.close()
	if typeof(data) != TYPE_DICTIONARY:
		return false

	var meta: Dictionary = data.get("meta", {}).get("pixelfx", {})
	var fps: float = float(meta.get("fps", 30.0))
	var should_loop: bool = bool(meta.get("loop", false))
	var frames_arr: Array = data.get("frames", [])

	var sf := SpriteFrames.new()
	if not sf.has_animation("default"):
		sf.add_animation("default")
	sf.set_animation_speed("default", fps)
	sf.set_animation_loop("default", should_loop)

	for item in frames_arr:
		var rect_d: Dictionary = item.get("frame", {})
		var atlas := AtlasTexture.new()
		atlas.atlas = tex
		atlas.region = Rect2(
			float(rect_d.get("x", 0)),
			float(rect_d.get("y", 0)),
			float(rect_d.get("w", 32)),
			float(rect_d.get("h", 32))
		)
		sf.add_frame("default", atlas)

	sprite_frames = sf
	if not should_loop and free_on_finish:
		if not animation_finished.is_connected(_on_done):
			animation_finished.connect(_on_done)
	return true

func _on_done() -> void:
	queue_free()
