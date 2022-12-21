import copy

from select import select
# from symbol import dotted_as_name
import turtle
import math
import random
from time import sleep
from sys import argv


class Sim:
	# Set true for graphical interface
	GUI = False
	screen = None
	selection = []
	turn = ''
	dots = []
	red = []
	blue = []
	available_moves = []
	minimax_depth = 0
	prune = False

	def __init__(self, minimax_depth, prune, gui):
		self.GUI = gui
		self.prune = prune
		self.minimax_depth = minimax_depth
		if self.GUI:
			self.setup_screen()

	def setup_screen(self):
		self.screen = turtle.Screen()
		self.screen.setup(800, 800)
		self.screen.title("Game of SIM")
		self.screen.setworldcoordinates(-1.5, -1.5, 1.5, 1.5)
		self.screen.tracer(0, 0)
		turtle.hideturtle()

	def draw_dot(self, x, y, color):
		turtle.up()
		turtle.goto(x, y)
		turtle.color(color)
		turtle.dot(15)

	def gen_dots(self):
		r = []
		for angle in range(0, 360, 60):
			r.append((math.cos(math.radians(angle)), math.sin(math.radians(angle))))
		return r

	def initialize(self):
		self.selection = []
		self.available_moves = []
		for i in range(0, 6):
			for j in range(i, 6):
				if i != j:
					self.available_moves.append((i, j))
		if random.randint(0, 2) == 1:
			self.turn = 'red'
		else:
			self.turn = 'blue'
		self.dots = self.gen_dots()
		self.red = []
		self.blue = []
		if self.GUI:
			turtle.clear()
		self.draw()

	def draw_line(self, p1, p2, color):
		turtle.up()
		turtle.pensize(3)
		turtle.goto(p1)
		turtle.down()
		turtle.color(color)
		turtle.goto(p2)

	def draw_board(self):
		for i in range(len(self.dots)):
			if i in self.selection:
				self.draw_dot(self.dots[i][0], self.dots[i][1], self.turn)
			else:
				self.draw_dot(self.dots[i][0], self.dots[i][1], 'dark gray')

	def draw(self):
		if not self.GUI:
			return 0
		self.draw_board()
		for i in range(len(self.red)):
			self.draw_line((math.cos(math.radians(self.red[i][0] * 60)), math.sin(math.radians(self.red[i][0] * 60))),
						   (math.cos(math.radians(self.red[i][1] * 60)), math.sin(math.radians(self.red[i][1] * 60))),
						   'red')
		for i in range(len(self.blue)):
			self.draw_line((math.cos(math.radians(self.blue[i][0] * 60)), math.sin(math.radians(self.blue[i][0] * 60))),
						   (math.cos(math.radians(self.blue[i][1] * 60)), math.sin(math.radians(self.blue[i][1] * 60))),
						   'blue')
		self.screen.update()
		sleep(1)

	def _evaluate(self):
		# TODO
		availables = copy.deepcopy(self.available_moves)
		if self.turn == 'red':
			selected_by_me = copy.deepcopy(self.red)
		else:
			selected_by_me = copy.deepcopy(self.blue)
		safe_available_moves = 0
		if not self.is_selctions_safe(selected_by_me):
			return -100
		while len(availables) > 0:
			new_selection = availables.pop()
			selected_by_me.append(new_selection)
			if self.is_selctions_safe(selected_by_me):
				safe_available_moves += 1
			selected_by_me.remove(new_selection)
		return safe_available_moves

	def is_selctions_safe(self, selections):
		if len(selections) < 3:
			return True
		selections.sort()
		for i in range(len(selections) - 2):
			for j in range(i + 1, len(selections) - 1):
				for k in range(j + 1, len(selections)):
					if selections[i][0] == selections[j][0] and selections[i][1] == selections[k][0] and selections[j][1] == selections[k][1]:
						return False
		return True

	def minimax(self, depth, player_turn):
		# TODO
		if player_turn == 'red':
			return self.normal_maximize(depth)
		else:
			return self.normal_minimize(depth)

	def normal_maximize(self, remaining_depth):
		res = self.gameover(self.red, self.blue)
		if remaining_depth == 0 or res != 0:
			return None, self._evaluate()

		possible_moves = self.available_moves
		max_score = float('-inf')

		if len(possible_moves) == 0:
			return None, 0

		for move in possible_moves:
			score = self.normal_minimize(remaining_depth - 1)[1]
			if score >= max_score:
				max_score, final_move = score, move

		return final_move, max_score

	def normal_minimize(self, remaining_depth):
		res = self.gameover(self.red, self.blue)
		if remaining_depth == 0 or res != 0:
			return None, self._evaluate()

		min_score = float('inf')
		possible_moves = self.available_moves

		if len(possible_moves) == 0:
			return None, 0

		for move in possible_moves:
			score = self.normal_maximize(remaining_depth - 1)[1]
			if score <= min_score:
				min_score, final_move = score, move

		return final_move, min_score

	def _swap_turn(self, turn):
		if turn == 'red':
			return 'blue'
		else:
			return 'red'

	def enemy(self):
		return random.choice(self.available_moves)

	def play(self):
		self.initialize()
		while True:
			if self.turn == 'red':
				# print(selection)
				# sleep(5)
				selection = self.minimax(depth=self.minimax_depth, player_turn=self.turn)[0]
				if selection[1] < selection[0]:
					selection = (selection[1], selection[0])
			else:
				selection = self.enemy()
				# print(selection)
				# sleep(5)
				if selection[1] < selection[0]:
					selection = (selection[1], selection[0])
			if selection in self.red or selection in self.blue:
				raise Exception("Duplicate Move!!!")
			if self.turn == 'red':
				self.red.append(selection)
			else:
				self.blue.append(selection)

			self.available_moves.remove(selection)
			self.turn = self._swap_turn(self.turn)
			selection = []
			self.draw()
			r = self.gameover(self.red, self.blue)
			if r != 0:
				return r

	def gameover(self, r, b):
		if len(r) < 3:
			return 0
		r.sort()
		for i in range(len(r) - 2):
			for j in range(i + 1, len(r) - 1):
				for k in range(j + 1, len(r)):
					if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
						return 'blue'
		if len(b) < 3:
			return 0
		b.sort()
		for i in range(len(b) - 2):
			for j in range(i + 1, len(b) - 1):
				for k in range(j + 1, len(b)):
					if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
						return 'red'
		return 0


if __name__ == "__main__":

	# game = Sim(minimax_depth=int(argv[1]), prune=True, gui=bool(int(argv[2])))
	game = Sim(minimax_depth=3, prune=False, gui=True)

	results = {"red": 0, "blue": 0}
	for i in range(10):
		print(i)
		results[game.play()] += 1

	print(results)
