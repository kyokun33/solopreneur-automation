extends Node2D

@onready var btn_test_sell: Button = $BtnTestSell

func _ready() -> void:
	btn_test_sell.pressed.connect(func():
		GameState.add_gold(50)
	)
