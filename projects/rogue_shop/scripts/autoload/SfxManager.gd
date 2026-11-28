extends Node

var sample_rate: float = 22050.0

func play_slash() -> void:
	_play_tone(520.0, 180.0, 0.10, -10.0)

func play_hit() -> void:
	_play_tone(210.0, 90.0, 0.09, -8.0)

func play_coin() -> void:
	_play_tone(980.0, 1320.0, 0.12, -10.0)

func play_capture() -> void:
	_play_tone(440.0, 880.0, 0.18, -9.0)

func play_levelup() -> void:
	_play_tone(523.0, 1046.0, 0.25, -8.0)

func _play_tone(freq_start: float, freq_end: float, duration: float, db: float) -> void:
	var player := AudioStreamPlayer.new()
	var gen := AudioStreamGenerator.new()
	gen.mix_rate = sample_rate
	gen.buffer_length = duration + 0.05
	player.stream = gen
	player.volume_db = db
	add_child(player)
	player.play()
	var pb := player.get_stream_playback() as AudioStreamGeneratorPlayback
	if pb:
		var frames := int(sample_rate * duration)
		var phase := 0.0
		for i in range(frames):
			var t := float(i) / float(frames)
			var freq := lerpf(freq_start, freq_end, t)
			var env := 1.0 - t
			phase += freq / sample_rate
			var sample := sin(phase * TAU) * env * 0.45
			pb.push_frame(Vector2(sample, sample))
	get_tree().create_timer(duration + 0.08).timeout.connect(player.queue_free)
