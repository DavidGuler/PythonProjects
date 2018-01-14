from consts import *

class speed(Vector2):

	def __init__(self, *args, **kwargs):
		super(speed, self).__init__(*args, **kwargs)
		self.angle = 0

	@property
	def direction(self):
		direction = round(self.angle.angle/90.0)*90
		if direction == -180:
			direction *= -1
		return direction

	@property
	def angle(self):
		return self.__angle

	@angle.setter
	def angle(self, value):
		if hasattr(self, "_speed__angle"):
			last_angle = self.__angle.angle
		else:
			last_angle = 0

		value %= 360
		if value > 180:
			self.__angle = angle(value - 360)
		else:
			self.__angle = angle(value)

		self.rotate_ip(self.__angle.angle - last_angle)

	def change_speed(self, acceleration):
		new_speed = self.length() + acceleration
		self.scale_to_length(new_speed)

	def turn(self, key_event):
		new_direction = DIRECTIONS[key_event]
		
		if abs(new_direction - self.direction) == 180:
			self.angle = self.angle.angle - self.angle.sign * 180
		else:
			comp_sign = angle(new_direction	 - self.angle.angle).sign
			self.angle = self.angle.angle + comp_sign * KEY_SENSITIVITY