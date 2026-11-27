extends Node2D

@onready var btn_go_dungeon: Button = $Panel/VBox/BtnGoDungeon

func _ready() -> void:
	btn_go_dungeon.pressed.connect(func():
		EventBus.scene_requested.emit("dungeon")
	)
