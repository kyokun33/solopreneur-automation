extends RefCounted
class_name AssetLoader

static var _cache: Dictionary = {}

static func load_tex(res_path: String) -> Texture2D:
	if _cache.has(res_path):
		return _cache[res_path]
	var tex: Texture2D = null
	if ResourceLoader.exists(res_path):
		var loaded = load(res_path)
		if loaded is Texture2D:
			tex = loaded
	if tex == null:
		var abs_path := ProjectSettings.globalize_path(res_path)
		if FileAccess.file_exists(abs_path):
			var img := Image.load_from_file(abs_path)
			if img and not img.is_empty():
				tex = ImageTexture.create_from_image(img)
	if tex != null:
		_cache[res_path] = tex
	return tex
