extends Node2D
class_name AmbientWorldFX

## Dave the Diver style living background layer:
## - Drifting dust/spores/bubbles
## - Breathing warm glow pools around torches/furnaces
## - Rising alchemy bubbles & forge sparks

@export var mode: String = "dungeon" # "dungeon", "shop", "workshop"

var particles: Array[Dictionary] = []
var glows: Array[Dictionary] = []
var t: float = 0.0

func setup(p_mode: String) -> void:
	mode = p_mode

func _ready() -> void:
	z_index = 2
	var count := 38 if mode == "dungeon" else 24
	for i in range(count):
		particles.append(_make_particle(true))

	if mode == "dungeon":
		for pos in [Vector2(190, 95), Vector2(1090, 95), Vector2(90, 520), Vector2(1190, 520)]:
			glows.append({"pos": pos, "radius": 115.0, "color": Color(1.0, 0.55, 0.15, 0.14), "phase": randf() * TAU})
	elif mode == "shop":
		for pos in [Vector2(445, 130), Vector2(730, 130), Vector2(1160, 140), Vector2(85, 510)]:
			glows.append({"pos": pos, "radius": 95.0, "color": Color(1.0, 0.68, 0.25, 0.13), "phase": randf() * TAU})
	elif mode == "workshop":
		glows.append({"pos": Vector2(145, 290), "radius": 140.0, "color": Color(1.0, 0.48, 0.12, 0.18), "phase": 0.0})
		glows.append({"pos": Vector2(445, 245), "radius": 90.0, "color": Color(0.25, 1.0, 0.45, 0.15), "phase": 1.2})

func _make_particle(random_y: bool) -> Dictionary:
	var pos := Vector2(randf_range(60.0, 1220.0), randf_range(80.0, 650.0) if random_y else 640.0)
	var vel := Vector2(randf_range(-14.0, 14.0), randf_range(-18.0, -6.0))
	var col := Color(0.45, 0.85, 1.0, 0.55)
	var sz := randf_range(2.0, 4.5)
	if mode == "shop":
		col = Color(1.0, 0.88, 0.48, 0.45)
		vel = Vector2(randf_range(-8.0, 8.0), randf_range(-10.0, -3.0))
	elif mode == "workshop":
		if randf() < 0.5:
			pos = Vector2(randf_range(100.0, 210.0), randf_range(220.0, 340.0))
			col = Color(1.0, 0.55, 0.15, 0.8)
			vel = Vector2(randf_range(-12.0, 12.0), randf_range(-42.0, -18.0))
		else:
			pos = Vector2(randf_range(410.0, 480.0), randf_range(210.0, 280.0))
			col = Color(0.35, 1.0, 0.5, 0.75)
			vel = Vector2(randf_range(-6.0, 6.0), randf_range(-28.0, -12.0))
	return {"pos": pos, "vel": vel, "col": col, "size": sz, "life": randf_range(1.5, 4.0)}

func _process(delta: float) -> void:
	t += delta
	for i in range(particles.size()):
		var p: Dictionary = particles[i]
		p["pos"] += p["vel"] * delta
		p["pos"].x += sin(t * 2.0 + float(i)) * 6.0 * delta
		p["life"] -= delta
		if p["life"] <= 0.0 or p["pos"].y < 50.0:
			particles[i] = _make_particle(false)
	queue_redraw()

func _draw() -> void:
	for g in glows:
		var pulse := 1.0 + sin(t * 3.5 + float(g["phase"])) * 0.10
		var c: Color = g["color"]
		var r: float = float(g["radius"]) * pulse
		for step in range(6):
			var frac := 1.0 - float(step) * 0.14
			draw_circle(g["pos"], r * frac, Color(c.r, c.g, c.b, c.a * 0.25))
	for p in particles:
		var alpha := clampf(float(p["life"]), 0.0, 1.0)
		var c: Color = p["col"]
		draw_rect(Rect2(p["pos"], Vector2(p["size"], p["size"])), Color(c.r, c.g, c.b, c.a * alpha))
