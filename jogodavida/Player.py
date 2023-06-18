#!/usr/bin/python
# -*- coding: UTF-8 -*-
from CareerType import CareerType
from constants import CHILD_HAVING_COST, CHILD_MONTHLY_EXPENSES, INIT_SALARY, NUM_CASAS, TOTAL_INIT_MONEY
from enums.ModifierType import ModifierType

class Player(object):
	def __init__(self, player_name, player_id, colour, player_interface):
		# Initial money-related values
		self.__salary = INIT_SALARY
		self.__total_money = TOTAL_INIT_MONEY
		self.__player_id = player_id
		# Multiplayer settings for identification
		self.__colour = colour
		self.__player_name = player_name
		self.__position = 0
		self.__char = None
		self.__properties = []
		# Career bonuses
		self.__career = CareerType.UNEMPLOYED
		self.__prop_discount_percentage = 0
		self.__bonus_rent = 0
		self.__bonus_salary = 0
		# Player interface for communicating with the UI in general when needed
		self._player_interface = player_interface
		# Control attributes
		self._is_first_move = True
		self.__nfam_members = 0
		self.__paid_rent_this_turn = False
		# State-related attributes
		self._can_roll_dice = True # FIXME: should be false for new players (testing purposes here)
		self._can_select_card = False
		self._can_pick_career = False
		self._can_select_property = False

	def get_properties_to_dict_move(self) -> dict:
		dict_move = {}
		i = 0
		for p in self.__properties:
			dict_move[i] = p.to_dict()
			i += 1
		return dict_move

	def get_paid_rent_this_turn(self):
		return self.__paid_rent_this_turn
	
	def set_paid_rent_this_turn(self, paid=True):
		self.__paid_rent_this_turn = paid

	def to_dict_move(self) -> dict:
		move_dict = { 
			"total_money": self.__total_money,
			"salary": self.__salary,
			# "colour": self.__colour,
			"position": self.__position,
			"is_first_move": self._is_first_move,
			"nfam_members": self.__nfam_members,
			"can_roll_dice": self._can_roll_dice,
			"can_select_card": self._can_select_card,
			"can_select_property": self._can_select_property,
			"can_pick_career": self._can_pick_career,
		}
		return move_dict

	def update(self, move : dict):
		message = f"Player {self.__player_name} made his move. "
		for key, val in move.items():
			if key == "career_attrs":
				if val["new_career"] == True:
					self.set_career(val["career"])
					message += "It's his first move, so he picked a career. "
			elif key == "normal_attrs":
				self.update_normal_attrs(val)
				message += "His updated attributes can be seen in the flashcards. "
			elif key == "rent_attrs":
				if val["paid_rent"]:
					message += f"He paid rent to {val['to']} and lost money. "
					# TODO: deal with rent owner
		return message

	# Used within DOG's receive_move method
	def update_normal_attrs(self, move : dict):
		self.__salary = move["salary"]
		self.__total_money = move["total_money"]
		self.__position = move["position"]
		# TODO: this one
		self._is_first_move = move["is_first_move"]
		self.__nfam_members = move["nfam_members"]
		self._can_roll_dice = move["can_roll_dice"]
		self._can_select_card = move["can_select_card"]
		self._can_pick_career = move["can_pick_career"]
		self._can_select_property = move["can_select_property"]

	def modify_state(self, state):		
		if state.type == ModifierType.SALARY:
			self.__salary += state.value
		elif state.type == ModifierType.TOTAL_MONEY:
			self.__total_money += state.value
		elif state.type == ModifierType.FAMILY:
			self.add_family_member(state.is_wife) # TODO: check what diagram has this and change it 

	def add_family_member(self, is_wife : bool):
		if is_wife and self.__nfam_members < 1:
			self._player_interface.show_messagebox_info("Marriage", f"Congratulations, you've been married! \
					       With this, your monthly income joins that of your wife's {self.__salary // 2}, and your\
							total money increases by {self.__total_money // 2}")
			self.__salary += self.__salary // 2
			self.__total_money += self.__total_money // 2
		elif is_wife and self.__nfam_members >= 1:
			self._player_interface.show_messagebox_info("Already married", "Fortunately (or unfortunately) for you, you are already married, and cannot have another wife. Skipping this turn.")
			return
		elif not is_wife and self.__nfam_members < 1:
			self._player_interface.show_messagebox_info("Cannot have baby", "Unfortunately, you cannot have a baby if you have no wife. Skipping this turn.")
			return
		elif not is_wife and self.__nfam_members < 4:
			self._player_interface.show_messagebox_info("Child birth", f"Congratulations, a child has been born in your family! \
					       With that, you pay the costs of the medical procedure ({CHILD_HAVING_COST}), and you have to spend {CHILD_MONTHLY_EXPENSES} more each month.")
			self.__salary -= CHILD_MONTHLY_EXPENSES
			self.__total_money -= CHILD_HAVING_COST
		else:
			self._player_interface.show_messagebox_info("Family full!", "You already have a full family, therefore you cannot add new members. Skipping this turn.")
			return
		self.__nfam_members += 1

	def update_position(self, steps : int):
		cur_pos = self.__position
		cur_pos = cur_pos + steps
		if cur_pos // NUM_CASAS > 0:
			cur_pos = 35 # last square. game should now be over in the main event handler
		self.__position = cur_pos

	def update_total_money(self, money : int):
		self.__total_money += money
	
	def set_can_roll_dice(self, val: bool):
		self._can_roll_dice = val

	def get_can_roll_dice(self) -> bool:
		return self._can_roll_dice

	def get_is_first_move(self) -> bool:
		return self._is_first_move
	
	def set_not_first_move(self):
		self._is_first_move = False

	def get_position(self) -> int:
		return self.__position
	
	def set_position(self, position: int):
		self.__position = position
	
	def get_colour(self):
		return self.__colour
	
	def set_char(self, char):
		self.__char = char

	def get_char(self):
		return self.__char
	
	def get_player_id(self) -> str:
		return self.__player_id
	
	def get_player_name(self) -> str:
		return self.__player_name 
	
	def set_career(self, career):
		if career == CareerType.FINANTIAL:
			self.__prop_discount_percentage = 0.15
			self.__bonus_rent = 0
			self.__bonus_salary = 0.20
		elif career == CareerType.NORMAL:
			self.__prop_discount_percentage = 0.05
			self.__bonus_rent = 0.30
			self.__bonus_salary = 0
		self.__career = career

	def receive_salary(self):
		self.__total_money += self.__salary + (self.__salary * self.__bonus_salary)

	def get_career(self):
		return self.__career
	
	def get_is_broke(self) -> bool:
		return self.__is_broke
	
	def get_total_money(self) -> int:
		return self.__total_money
	
	def set_total_money(self, total_money):
		self.__total_money = total_money

	def get_salary(self) -> int:
		return self.__salary
	
	def get_nfam_members(self) -> int:
		return self.__nfam_members
	
	def get_properties(self):
		return self.__properties
	
	def get_property_discount(self) -> float:
		return self.__prop_discount_percentage
	
	def get_bonus_rent(self) -> float:
		return self.__bonus_rent
	
	def get_bonus_salary(self) -> float:
		return self.__bonus_salary

	def get_card_content(self):
		career_name = ""
		if self.__career == CareerType.FINANTIAL:
			career_name = "Finantial"
		elif self.__career == CareerType.NORMAL:
			career_name = "Normal"
		else:
			career_name = "Unemployed"
		return [
			{ 'field': 'Bank', 'value': f'U$$ {self.__total_money}' },
			{ 'field': 'Salary', 'value': f'U$$ {self.__salary}' },
			{ 'field': 'Family members', 'value': f'{self.__nfam_members}' },
			{ 'field': 'Career', 'value': f'{career_name}' },
			{ 'field': 'Number of properties', 'value': f'{len(self.__properties)}' },
			{ 'field': 'Current square', 'value': f'{self.__position+1}'}
		]
