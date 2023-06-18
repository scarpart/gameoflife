#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
from ModifierCard import ModifierCard
import Player
from PropertyCard import PropertyCard
from cards_data import CARDS_DATA
from constants import LARGURA_CASA, NUM_CASAS
from tkinter import NW
from Player import Player
from enums.ModifierType import ModifierType
from utils.get_board_house_coordinates import get_board_house_coordinates
from utils.lowercase_and_underscore import lowercase_and_underscore

class Game(object):
	def __init__(self, player_interface):
		self.players = None
		self.dice = None
		self.turns = 0
		self.player_turn = None
		self.local_player_id = ""
		self.__player_interface = player_interface
		# changed something here (used to be arg player_interface)
		self.winner = None

		self.cards_on_squares = [[] for _ in range(NUM_CASAS)]
		self.all_cards = self.create_all_cards()
		self.position_cards = self.create_position_cards()
		self.distribute_cards_on_squares()

	def handle_pick_career(self):
		self.__player_interface.show_career_options()

	def handle_dice_roll(self):
		can_roll = self.player_turn.get_can_roll_dice()
		# print("local player id dice roll", self.local_player_id)
		# print("player turn id dice roll", self.player_turn.get_player_id())
		if not can_roll or self.local_player_id != self.player_turn.get_player_id():
			self.__player_interface.show_messagebox_info("Not your turn!", "It's not your turn to play.")
			return
		
		# TODO: diagrams
		local_actor = self.__player_interface.get_local_actor()
		
		is_first_move = self.player_turn.get_is_first_move()
		if is_first_move:
			self.handle_pick_career() 
			self.player_turn.set_not_first_move()
			self.__player_interface.refresh_ui() # TODO: add to diagrams

			career_move = self.get_career_move()
			self.player_turn = self.get_next_player_turn()
			self.__player_interface.update_current_player_text()
			local_actor.send_move(career_move) 
			return
		
		self.__player_interface.show_messagebox_info("Salary received.", f"For your work this month, you are receiving {self.player_turn.get_salary()} with a bonus of {self.player_turn.get_bonus_salary()*self.player_turn.get_salary()}")
		self.player_turn.receive_salary()
		self.__player_interface.refresh_ui()
		self.update_turn()
		
		steps = self.dice.roll()
		self.player_turn.update_position(steps)
		self.dice.draw(steps)
		self.board.update_player_position(self.player_turn)
		
		position = self.player_turn.get_position()
		# TODO: change below to square_by_position
		landed_square = self.board.get_squares()[position]
		if landed_square.has_owner() and landed_square.get_owner() != self.player_turn:
			self.__handle_property_owned(landed_square)
			self.player_turn.set_paid_rent_this_turn(True)
		else:
			self.player_turn.set_paid_rent_this_turn(False)

		self.handle_select_card() 

		# TODO: update diagrams with below
		game_over, winner = self.check_if_game_over()
		if game_over:
			endgame_move = self.get_endgame_move(winner)
			local_actor.send_move(endgame_move)
			self.handle_game_end(winner.get_player_id())
			return 
		
		# FIXME: diagrams
		self.__player_interface.refresh_ui()
		move = self.get_roll_dice_move()
		self.player_turn = self.get_next_player_turn()
		self.__player_interface.update_current_player_text()
		local_actor.send_move(move)

	def handle_move(self, move : dict):
		if move["match_status"] == "finished":
			self.handle_game_end(move["winner"])
		elif move["match_status"] == "next":
			self.update_game_with_move(move["actions"])
			self.update_ui_with_move(move["ui_actions"])
			print("Current player_id", self.player_turn.get_player_id())
			self.player_turn = self.get_player_by_id(move["next_player"])
			print("Received player_id", self.player_turn.get_player_id())
			self.__player_interface.update_current_player_text()

	def handle_game_end(self, winner):
		winner = self.get_player_by_id(winner)
		if self.local_player_id == winner.get_player_id():
			self.__player_interface.render_win_screen(winner)
		else:
			self.__player_interface.render_loss_screen(winner)

	def get_player_by_id(self, id: str) -> Player:
		for player in self.players:
			if player.get_player_id() == id:
				return player
		return None

	def update_ui_with_move(self, move : dict):
		for _, val in move["property_attrs"].items():
			owner = self.get_player_by_id(val["owner"])
			prop = self.board.get_square_by_position(val["position"])
			
			print("\nin update UI with move: ", val["owner"], owner)

			# TODO: check if squares are appropriate (position and all)

			prop.set_owner(owner)
			property_icon = prop.add_property_icon()
			position = get_board_house_coordinates(val["position"])
			self.create_property_image(property_icon, position)
			prop.set_fees(val["fees"])
			properties = owner.get_properties()
			properties.append(prop)

	def update_game_with_move(self, move : dict):
		for player_id, attr in move.items():
			player = self.get_player_by_id(player_id)
			print("\n\nIn update game with move:", player_id, player)
			# please work
			print(attr)
			message = player.update(attr)
			self.__player_interface.show_messagebox_info("Move made", message)
		self.__player_interface.refresh_ui()

	def get_player_by_name(self, player_name) -> Player:
		for player in self.players:
			if player.get_player_name() == player_name:
				return player
		return None

	def get_endgame_move(self, winner : Player):
		move = {
			"match_status": "finished",
			"winner": winner.get_player_id(),	
		}
		return move

	def get_career_move(self) -> dict:
		move = {
			"match_status": "next",
			"actions": {
				self.player_turn.get_player_id(): {
					"career_attrs": {
						"new_career": True,
						"career": self.player_turn.get_career()
					}
				} 
			},
			"ui_actions": {
				"property_attrs": self.player_turn.get_properties_to_dict_move()
			},
			"next_player": self.get_next_player_turn().get_player_id()
		}
		return move

	# TODO: handle case in which there is a property and bro stepped on it.
	def get_roll_dice_move(self) -> dict:
		move = {
			"match_status": "next",
			"actions": {
				self.player_turn.get_player_id(): {
					"career_attrs": {
						"new_career": False,
						"career": self.player_turn.get_career(),
					},
					"normal_attrs": self.player_turn.to_dict_move(),
					"rent_attrs": {
						"paid_rent": self.player_turn.get_paid_rent_this_turn(),
						"to": "someone_idk" 
					}, 
					# ONGOING: making the player.to_dict method
				}
			},
			"ui_actions": {
				"property_attrs": self.player_turn.get_properties_to_dict_move()
			},
			"next_player": self.get_next_player_turn().get_player_id()
		}
		return move

	def __handle_property_owned(self, landed_square):
		"""NOTE: This method is in the roll dice diagram"""
		owner = landed_square.get_owner()
		
		fee = landed_square.get_property_fees()
		percentage = owner.get_property_discount() 
		fee = fee + (fee * percentage)

		self.player_turn.update_total_money(-fee)
		owner.update_total_money(fee)

		title = "Property Owned"
		text = f"You landed on a property that is owned by {owner.get_player_name()}. A fee of {fee} has been deducted from your total money." 
		self.__player_interface.show_messagebox_info(title, text)

	# TODO: diagram for this functionality
	def handle_select_card(self):
		dialog = self.__player_interface.show_card_options() # we have handle_card_choice here as well
		master = self.__player_interface.get_master()
		master.wait_window(dialog)

	def create_property_image(self, image, position):
		x = position[0] + LARGURA_CASA * 0.1
		y = position[1] + LARGURA_CASA * 0.1
		self.board.canvas.create_image((x, y), image=image, anchor=NW)

	def update_turn(self):
		self.turns += 1

	def check_if_game_over(self) -> tuple:
		game_over = False
		winner = None
		for player in self.players:
			if player.get_total_money() <= 0 or player.get_position() >= NUM_CASAS-1:
				game_over = True
		if game_over:
			max_money = 0
			for player in self.players:
				if player.get_total_money() > max_money:
					winner = player
		return game_over, winner

	# """FIXME: deletar essa coisa :("""
	# def update_game_state(self, data: dict):
	# 	self.dice.number = data['dice']
	# 	# Provavelmente n precisa disso
	# 	# self.turns = data['turns']

	# 	for player_data in data['players']:
	# 		# FIXME: error in find_player, said player not found...
	# 		# self.game.find_player(self.player_name <-- here)
	# 		player = self.find_player(player_data['player_id'])
	# 		player.update(player_data)

	# 	self.player_turn = self.find_player(data['player_turn']['player_id'])

	"""FIXME: deletar provavelmente varios abaixo"""	
	def get_next_player_turn(self) -> Player:
		next_player = self.players[0]
		player_index = self.players.index(self.player_turn)
		players_length = len(self.players)

		next_player = self.players[(player_index + 1) % players_length]
		
		# print("\n\nThe next player should be this fella:")
		# print(next_player.get_player_name())
		
		return next_player

	def _create_players(self, players) -> list[Player]:
		colors = ['red','yellow', 'blue']
		instances = []
		for i, player_list in enumerate(players):
			# TODO: find by id? player name?
			print("Players: ", players)
			player_name = lowercase_and_underscore(player_list[0])
			instances.append(Player(player_name, player_list[1], colors[i % len(colors)], self.__player_interface))
		# This is wrong innit?
		self.player_turn = instances[0]
		return instances

	# FIXME: deletar abaixo
	# def find_player(self, player_name: str) -> Player:
	# 	player_name_underscore= lowercase_and_underscore(player_name)
	# 	for player in self.players:
	# 		if player.get_player_name() == player_name_underscore:
	# 			return player
	# 	raise ValueError('Player was not found')
		
	def to_dict(self):
		return {
			'players': [player.to_dict() for player in self.players],
			'dice': self.dice.number,
			'turns': self.turns,
			'player_turn': self.player_turn.to_dict()
		}

	def set_board(self, board):
		self.board = board

	def set_local_player_id(self, local_player_id : str):
		self.local_player_id = local_player_id

	def get_local_player_id(self) -> str:
		return self.local_player_id

	def start_game(self):
		local_actor = self.__player_interface.get_local_actor()
		start_status = local_actor.start_match(number_of_players=2)
		code = start_status.get_code()
		message = start_status.get_message()
		players = None

		if code == '0' or code == '1':
			self.__player_interface.show_messagebox_info("Start error", message) # TODO:
			return
		elif code == '2':
			self.local_player_id = start_status.get_local_id()
			players = start_status.get_players()
		
		self.__player_interface.show_messagebox_info("Game started", message) 

		# FIXME: provavelmente está errado render_game_interface ser aqui
		self.__player_interface.render_game_interface(players)

	def set_players(self, players):
		self.players = self._create_players(players)

	def get_players(self):
		return self.players

	def set_dice(self, dice):
		self.dice = dice

	def get_player_turn(self) -> Player:
		return self.player_turn

	# TODO: put this method and the other associated ones as methods of the board class	
	def distribute_cards_on_squares(self):
		random.shuffle(self.all_cards)
		card_groups = [self.all_cards[i:i+3] for i in range(0, len(self.all_cards), 3)]
		card_groups *= (NUM_CASAS // len(card_groups)) + 1
		for i in range(NUM_CASAS):
			self.cards_on_squares[i] = card_groups[i]

	def create_all_cards(self):
		all_cards = []
		for name, desc, modif, mod_type, times_picked in CARDS_DATA:
			if mod_type == ModifierType.PROPERTY:
				all_cards.append(PropertyCard(name, desc, modif, mod_type, times_picked=times_picked))
			else:
				all_cards.append(ModifierCard(name, desc, modif, mod_type, times_picked=times_picked))
		random.shuffle(all_cards)
		return all_cards
	
	def get_cards_for_position(self, position):
		return self.position_cards[position]
	
	def create_position_cards(self):
		num_positions = 40  
		position_cards = {}

		random.shuffle(self.all_cards)
		available_cards = self.all_cards.copy()

		# This is for testing purposes and should be eliminated soon TODO: that
		assert len(available_cards) >= num_positions, "Not enough cards for all positions"

		for position in range(num_positions):
			position_cards[position] = []
			for _ in range(3):
				while True: 
					card = random.choice(available_cards)
					if card not in position_cards[position]:
						break

				position_cards[position].append(card)
				if card.times_picked >= 3:
					available_cards.remove(card)
				
				card.times_picked += 1

		return position_cards
	
	def get_winner(self) -> Player:
		return self.winner

	def get_board(self):
		return self.board

	def get_dice(self):
		return self.dice
