#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
from ModifierCard import ModifierCard
import Player
from PlayerState import PlayerState
from PropertyCard import PropertyCard
from cards_data import CARDS_DATA
from constants import LARGURA_CASA, NUM_CASAS, PLAYER_AMOUNT, PROPERTY_FEE
from tkinter import NW
import tkinter as tk
from Player import Player
from enums.ModifierType import ModifierType
from utils.get_board_house_coordinates import get_board_house_coordinates
from utils.lowercase_and_underscore import lowercase_and_underscore


class Game(object):
	def __init__(self, player_interface):
		self.__players = None
		self.__dice = None
		self.__player_turn = None
		self.__local_player_id = ""
		self.__player_interface = player_interface
		# changed something here (used to be arg player_interface)
		self.__winner = None
		self.__board = None

		self.__cards_on_squares =  [[] for _ in range(NUM_CASAS)]
		self.__all_cards = self.__create_all_cards()
		self.__position_cards = self.__create_position_cards()
		self.__distribute_cards_on_squares()

	def __handle_pick_career(self):
		self.__player_interface.show_career_options()

	def handle_dice_roll(self):
		can_roll = self.__player_turn.get_can_roll_dice()
		if not can_roll or self.__local_player_id != self.__player_turn.get_player_id():
			self.__player_interface.show_messagebox_info("Not your turn!", "It's not your turn to play.")
			return
		
		local_actor = self.__player_interface.get_local_actor()
		
		is_first_move = self.__player_turn.get_is_first_move()
		if is_first_move:
			self.__player_turn.set_player_state(PlayerState.PICKING_CAREER)
			self.__handle_pick_career() 
			self.__player_turn.set_not_first_move()
			self.__player_interface.refresh_ui() 

			self.__player_turn.set_player_state(PlayerState.NOT_TURN)
			career_move = self.__get_move_to_send()
			self.__player_turn = self.__get_next_player_turn()
			self.__player_interface.update_current_player_text()			
			local_actor.send_move(career_move) 
			return
		
		self.__player_turn.set_player_state(PlayerState.SELECTING_CARD)
		self.__player_interface.show_messagebox_info("Salary received.", f"For your work this month, you are receiving {self.__player_turn.get_salary()} with a bonus of {self.__player_turn.get_bonus_salary()*self.__player_turn.get_salary()}")
		self.__player_turn.receive_salary()
		self.__player_interface.refresh_ui()
		
		steps = self.__dice.roll()
		self.__player_turn.update_position(steps)
		self.__dice.draw(steps)
		self.__board.update_player_position(self.__player_turn)
		
		position = self.__player_turn.get_position()
		landed_square = self.__board.get_square_by_position(position+1) # Esse +1 é por conveniência, mas funciona (tem a ver com a indexação que estamos usando)
		if landed_square.has_owner() and landed_square.get_owner() != self.__player_turn:
			self.__handle_property_owned(landed_square)
		else:
			self.__player_turn.set_paid_rent_this_turn(False)
			self.__player_turn.set_rent_owner("")
			self.__player_turn.set_paid_rent_amount(0)

		self.__handle_select_card() 

		game_over, winner = self.__check_if_game_over()
		if game_over:
			endgame_move = self.__get_endgame_move(winner)
			local_actor.send_move(endgame_move)
			self.__handle_game_end(winner.get_player_id())
			return 
		
		self.__player_turn.set_player_state(PlayerState.NOT_TURN)
		self.__player_interface.refresh_ui()
		move = self.__get_move_to_send()
		self.__player_turn = self.__get_next_player_turn()
		self.__player_interface.update_current_player_text()
		local_actor.send_move(move)

	def handle_move(self, move : dict):
		if move["match_status"] == "finished":
			self.__handle_game_end(move["winner"])
		elif move["match_status"] == "next":
			self.__update_game_with_move(move["actions"])
			self.__update_ui_with_move(move["ui_actions"])
			self.__update_rent_action_with_move(move["rent_game_actions"])
			self.__player_turn = self.get_player_by_id(move["next_player"])
			self.__player_interface.update_current_player_text()

	def __update_rent_action_with_move(self, move : dict):
		if move["paid_rent"]:
			owner = self.get_player_by_id(move["to"])
			print("[receive] Owner of property (to receive money!):", owner)
			print("[receive] Owner's previous money amount:", owner.get_total_money())
			owner_money = owner.get_total_money()
			owner.set_total_money(owner_money + move["paid_rent_amount"])
			print("[receive] Owner's new money amount:", owner.get_total_money())

	def __handle_game_end(self, winner):
		winner = self.get_player_by_id(winner)
		if self.__local_player_id == winner.get_player_id():
			local_player = self.get_player_by_id(self.__local_player_id)
			local_player.set_player_state(PlayerState.WINNER)
			self.__player_interface.render_win_screen(winner)
		else:
			local_player = self.get_player_by_id(self.__local_player_id)
			local_player.set_player_state(PlayerState.LOSER)
			self.__player_interface.render_loss_screen(winner)

	def get_player_by_id(self, id: str) -> Player:
		for player in self.__players:
			if player.get_player_id() == id:
				return player
		return None

	def __update_ui_with_move(self, move : dict):
		for _, val in move["property_attrs"].items():
			owner = self.get_player_by_id(val["owner"])
			prop = self.__board.get_square_by_position(val["position"]+1) # esse +1 é pq a posição vem com índice 0 

			prop.set_owner(owner)

			print("\nPosition of square in receive move:", prop.get_position())
			print("Onwer of square in receive move:", prop.get_owner())

			property_icon = prop.add_property_icon()
			position = get_board_house_coordinates(val["position"])
			self.create_property_image(property_icon, position)
			prop.set_fees(val["fees"])
			properties = owner.get_properties()
			properties.append(prop)

	def __update_game_with_move(self, move : dict):
		for player_id, attr in move.items():
			player = self.get_player_by_id(player_id)
			# Esse rent_owner_name é mais por conveniência e não precisar de uma 
			# referência à classe Game dentro de Player, se não seria muito acoplamento...
			rent_owner_name = self.get_player_by_id(move[player_id]["rent_attrs"]["to"])
			if rent_owner_name:
				rent_owner_name = rent_owner_name.get_player_name()
			message = player.update(attr, rent_owner_name)
			self.__player_interface.show_messagebox_info("Move made", message)
		self.__player_interface.refresh_ui()

	def get_player_by_name(self, player_name) -> Player:
		for player in self.__players:
			if player.get_player_name() == player_name:
				return player
		return None

	def __get_endgame_move(self, winner : Player):
		move = {
			"match_status": "finished",
			"winner": winner.get_player_id(),	
		}
		return move

	def __get_move_to_send(self) -> dict:
		move = {
			"match_status": "next",
			"actions": {
				self.__player_turn.get_player_id(): {
					"career_attrs": {
						"new_career": True,
						"career": self.__player_turn.get_career()
					},
					"rent_attrs": {
						"paid_rent": self.__player_turn.get_paid_rent_this_turn(),
						"to": self.__player_turn.get_rent_owner(),
						"paid_rent_amount": self.__player_turn.get_paid_rent_amount()
					}, 
					"normal_attrs": self.__player_turn.to_dict_move(),
				} 
			},
			"rent_game_actions": {
				"paid_rent": self.__player_turn.get_paid_rent_this_turn(),
				"to": self.__player_turn.get_rent_owner(),
				"paid_rent_amount": self.__player_turn.get_paid_rent_amount()
			}, 
			"ui_actions": {
				"property_attrs": self.__player_turn.get_properties_to_dict_move()
			},
			"next_player": self.__get_next_player_turn().get_player_id()
		}
		return move

	def __handle_property_owned(self, landed_square):
		owner = landed_square.get_owner()
		
		fee = landed_square.get_property_fees()
		percentage = owner.get_property_discount() 
		fee = fee + (fee * percentage)

		self.__player_turn.update_total_money(-fee)
		owner.update_total_money(fee)
		self.__player_turn.set_rent_owner(owner.get_player_id())
		self.__player_turn.set_paid_rent_amount(fee)
		self.__player_turn.set_paid_rent_this_turn(True)

		title = "Property Owned"
		text = f"You landed on a property that is owned by {owner.get_player_name()}. A fee of {fee} has been deducted from your total money." 
		self.__player_interface.show_messagebox_info(title, text)

	def __handle_select_card(self):
		dialog = self.__player_interface.show_card_options() # we have handle_card_choice here as well
		master = self.__player_interface.get_master()
		master.wait_window(dialog)

	def select_card(self, card, dialog):
		# Essas checagens só estão aqui para propósitos de organização
		# Isso foi feito de um jeito que seria mais intelegível em um diagrama
		# (devido à natureza meio estranha de lidar com callbacks em botões, e de termos que lidar com o select_property) 
		is_property_card = isinstance(card, PropertyCard)
		if is_property_card:
			self.__player_turn.set_player_state(PlayerState.SELECTING_PROPERTY)
			nested_dialog = self.handle_select_property()
			master = self.__player_interface.get_master()
			master.wait_window(nested_dialog)
			percentage = self.__player_turn.get_property_discount()
			self.__player_turn.update_total_money(card.property.value + (percentage * card.property.value))
		else:
			card.apply_effect(self.__player_turn)

		self.__player_turn.set_player_state(PlayerState.CHOSE_CARD)
		dialog.destroy()   

	# Esse método atualiza bastante a GUI, mas é essencialmente um método de lógica de jogo
	# Logo, colocamos ele aqui na classe Game. O mesmo pode ser dito para alguns outros métodos.
	def handle_select_property(self) -> tk.Toplevel:
		master = self.__player_interface.get_master()
		dialog = tk.Toplevel(master)
		dialog.title("Select a property")

		num_columns = 3
		row = 0
		col = 0

		squares = self.__board.get_active_squares()

		for i, square in enumerate(squares):
			owner = square.get_owner()
			if owner is None:
				button_text = f"Position: {i+2}" # FIXME: this may cause some issues
				button = tk.Button(dialog, text=button_text,
								command=lambda s=square: self.select_property(s, dialog))
				button.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

				col += 1
				if col >= num_columns:
					col = 0
					row += 1

		for i in range(num_columns):
			dialog.columnconfigure(i, weight=1)
		for i in range(row + 1):
			dialog.rowconfigure(i, weight=1)

		return dialog
	
	def select_property(self, square, dialog):       
		if not self.__player_turn.get_can_select_property():
			return
		properties = self.__player_turn.get_properties()
		properties.append(square)
		square.set_owner(self.__player_turn)
		property_icon = square.add_property_icon()
		position = square.get_position()
		self.create_property_image(property_icon, position)
		square.set_fees(PROPERTY_FEE)
		dialog.destroy() 

	def create_property_image(self, image, position):
		x = position[0] + LARGURA_CASA * 0.1
		y = position[1] + LARGURA_CASA * 0.1
		self.__board.get_canvas().create_image((x, y), image=image, anchor=NW)

	def __check_if_game_over(self) -> tuple:
		game_over = False
		winner = None
		for player in self.__players:
			if player.get_total_money() <= 0 or player.get_position() >= NUM_CASAS-1:
				game_over = True
		if game_over:
			max_money = 0
			for player in self.__players:
				if player.get_total_money() > max_money:
					winner = player
		return game_over, winner

	def __get_next_player_turn(self) -> Player:
		next_player = self.__players[0]
		player_index = self.__players.index(self.__player_turn)
		players_length = len(self.__players)

		next_player = self.__players[(player_index + 1) % players_length]
		
		return next_player

	def __create_players(self, players):
		print("IN CREATE PLAYERS - ISSUE?")
		colors = ['red','yellow', 'blue']
		instances = []
		for i, player_list in enumerate(players):
			player_name = lowercase_and_underscore(player_list[0])
			instances.append(Player(player_name, player_list[1], player_list[2], colors[int(player_list[2]) % len(colors)], self.__player_interface))
		instances.sort(key=lambda x: x.get_priority())
		# This is wrong innit?
		self.__player_turn = instances[0]
		return instances

	def set_board(self, board):
		self.__board = board

	def set_local_player_id(self, local_player_id : str):
		self.__local_player_id = local_player_id

	def get_local_player_id(self) -> str:
		return self.__local_player_id

	def start_game(self):
		local_actor = self.__player_interface.get_local_actor()
		start_status = local_actor.start_match(number_of_players=PLAYER_AMOUNT)
		code = start_status.get_code()
		message = start_status.get_message()
		players = None

		if code == '0' or code == '1':
			self.__player_interface.show_messagebox_info("Start error", message)
		elif code == '2':
			self.__local_player_id = start_status.get_local_id()
			players = start_status.get_players()
			self.__player_interface.show_messagebox_info("Game started", message) 
			self.__player_interface.render_game_interface(players)

	def set_players(self, players):
		self.__players = self.__create_players(players)

	def get_players(self):
		return self.__players

	def set_dice(self, dice):
		self.__dice = dice

	def get_player_turn(self) -> Player:
		return self.__player_turn

	# TODO: put this method and the other associated ones as methods of the board class	
	def __distribute_cards_on_squares(self):
		random.shuffle(self.__all_cards)
		card_groups = [self.__all_cards[i:i+3] for i in range(0, len(self.__all_cards), 3)]
		card_groups *= (NUM_CASAS // len(card_groups)) + 1
		for i in range(NUM_CASAS):
			self.__cards_on_squares[i] = card_groups[i]

	def __create_all_cards(self):
		__all_cards = []
		for name, desc, modif, mod_type, times_picked in CARDS_DATA:
			if mod_type == ModifierType.PROPERTY:
				__all_cards.append(PropertyCard(name, desc, modif, mod_type, times_picked=times_picked))
			else:
				__all_cards.append(ModifierCard(name, desc, modif, mod_type, times_picked=times_picked))
		random.shuffle(__all_cards)
		return __all_cards
	
	def get_cards_for_position(self, position):
		return self.__position_cards[position]
	
	def __create_position_cards(self):
		num_positions = 40  
		__position_cards = {}

		random.shuffle(self.__all_cards)
		available_cards = self.__all_cards.copy()

		for position in range(num_positions):
			__position_cards[position] = []
			for _ in range(3):
				while True: 
					card = random.choice(available_cards)
					if card not in __position_cards[position]:
						break

				__position_cards[position].append(card)
				if card.times_picked >= 3:
					available_cards.remove(card)
				
				card.times_picked += 1

		return __position_cards
	
	def get_winner(self) -> Player:
		return self.__winner

	def get_board(self):
		return self.__board

	def get_dice(self):
		return self.__dice
