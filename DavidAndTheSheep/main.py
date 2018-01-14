from consts import *
from speed import speed

def change_frame(screen, characters):
	screen.fill(DEFAULT_SCREEN_COLOR)
	for character, character_rect in characters.items():
		screen.blit(character, character_rect)

	display.flip()

def change_loc(character, move_vec):
	character.centerx += move_vec.x
	character.centery += move_vec.y
	return character

def move_character(character, move_vec):
	angle = move_vec.angle
	
	sample_rect = change_loc(character.copy(), move_vec)
	collide_border = sample_rect.collidelist(game_borders.BORDERS)
	print("{0}, {1}, {2}, {3}, {4}".format(sample_rect.right, sample_rect.left, game_borders.SCREEN_SIZE[0], game_borders.SCREEN_SIZE[1], collide_border))

	if collide_border != -1:
		print("Collied")
		if collide_border in (1,3):
			move_vec.angle = -angle.angle
		else:
			move_vec.angle = angle.sign * (180 - abs(angle.angle))

		#print("speed is: {0},{1} and angle {2}".format(move_vec.x, move_vec.y, move_vec.angle.angle))
		character = change_loc(character, move_vec)

	else:
		character = sample_rect

	return character

def get_next_event():
	game_events = event.get()
	for game_event in game_events:
		yield game_event

def main():
	screen = display.set_mode(game_borders.SCREEN_SIZE)
	davids_hair = image.load(HERO_IMG)
	key_type = None

	davids_hair_rect = davids_hair.get_rect()
	davids_hair_rect.inflate_ip(*INIT_SIZE_REDUCTION)
	davids_hair_rect = davids_hair_rect.move(INIT_LOC)
	davids_speed = speed(INIT_SPEED)

	characters = {davids_hair: davids_hair_rect}
	change_frame(screen, characters)

	game_events_handler = get_next_event()
	print("Start Game")

	while 1:
		time.sleep(0.01)
		try:
			game_event = next(game_events_handler)
		except StopIteration:
			game_events_handler = get_next_event()

		if game_event.type == QUIT:
			sys.exit()
		elif game_event.type == KEYDOWN:
			key_type = game_event.key
		elif game_event.type == KEYUP:
			key_type = None

		if key_type == K_SPACE:
			davids_speed.change_speed(KEY_SENSITIVITY)

		elif key_type in DIRECTIONS.keys():
			davids_speed.turn(key_type)
			print ("x:{0}, y:{1}, angle:{2}".format(
				davids_speed.x, davids_speed.y, davids_speed.angle.angle))

		characters[davids_hair] = move_character(characters[davids_hair], davids_speed)
		change_frame(screen, characters)

if __name__ == "__main__":
	main()

