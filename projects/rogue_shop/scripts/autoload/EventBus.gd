extends Node

signal scene_requested(scene_name: String)
signal gold_changed(new_gold: int)
signal day_changed(new_day: int)
signal craft_skill_changed(new_level: int, xp: int)
signal inventory_changed()
signal log_message(text: String)
