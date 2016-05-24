#
#
#
#
#
#
# Warning: This program written by a non-professional programmer. 
# This is not the best piece of software that was written today.
# Constructive criticism and updates welcome!
#
# --Chris
#
#
#
#

# Input some cards that define your deck (up to 5)
# Program searches using http://sales.starcitygames.com/deckdatabase/index.php
#	I might learn some html/python here
# Program parses out all the decklists by reading the html
# Program somehow tells us what the most common card choices are
# 	will need to somehow sort the decks into classes of some kind; I might learn some linear algebra here

import datetime
import os

class DeckList:
	# A DeckList is a dictionary of cards in the maindeck and a dictionary of cards in the sideboard.

	def __init__(self):
		self.date = ''
		self.event = ''
		self.pilot = ''
		self.deckname = ''
		self.place = ''
		self.maindeck = {}
		self.sideboard = {}
		self.seventyfive = {}

	def __repr__(self):
		outputString = ''

		outputString += self.deckname + ' '
		outputString += 'piloted by ' + self.pilot + ' '
		outputString += 'at ' + self.event + ' '
		outputString += 'on ' + self.date + '\n'

		outputString += 'Main deck: \n'
		for cardname in self.maindeck:
			outputString += str(self.maindeck[cardname]) + 'x ' + cardname + '\n'
		outputString += 'Sideboard: \n'
		for cardname in self.sideboard:
			outputString += str(self.sideboard[cardname]) + 'x ' + cardname + '\n'
		outputString += 'Seventy-five: \n'
		for cardname in self.seventyfive:
			outputString += str(self.seventyfive[cardname]) + 'x ' + cardname + '\n'


		return outputString

	def addmaindeckcard(self, cardname, number):
		self.maindeck[cardname] = int(number)
		self.addtoseventyfive(cardname, number)

	def addsideboardcard(self, cardname, number):
		self.sideboard[cardname] = int(number)
		self.addtoseventyfive(cardname, number)

	def addtoseventyfive(self, cardname, number):
		if cardname in self.seventyfive:
			self.seventyfive[cardname] += int(number)
		else:
			self.seventyfive[cardname] = int(number)


def distance(decklist1, decklist2):
	# How many cards do you have to change to get from decklist 1 to decklist 2?
	distance = 0

	for card in decklist1.seventyfive:
		if card in decklist2.seventyfive:
			distance += (abs(decklist1.seventyfive[card] - decklist2.seventyfive[card]))
		else:
			distance += decklist1.seventyfive[card]
	for card in decklist2.seventyfive:
		if card not in decklist1.seventyfive:
			distance += decklist2.seventyfive[card]
	
	distance = distance/2

	return distance



def parseDecklist(filename):
	# We need to read through the HTML file from starcity and grab the amounts of each card.

	inputfile = open('decks/'+filename)
	decklist = DeckList()

	maindeck_flag = True 	# The cards appearing first will be in the maindeck, but if we ever hit the word "sideboard," then we should trip the flag.
		
	for line in inputfile:
		# We want to find all the cards listed in the file. They appear as strings like 
		# <li>4 <a href="http://sales.starcitygames.com/cardsearch.php?singlesearch=Bounding+Krasis" rel="http://static.starcitygames.com/sales//cardscans/MTG/ORI/en/nonfoil/BoundingKrasis.jpg" target="new">Bounding Krasis</a></li>
		#                * <-- position_of_indicator                                               * <-- position_of_end_of_card

		# If we find the sideboard indicator, then trip the flag so future cards will appear in the sideboard.
		if line[0:43] == '<h3 class="decklist_heading">Sideboard</h3>':
			maindeck_flag = False

		# If we find the name of the deck, use that.
		if line[0:27] == '<header class="deck_title">':
			beginning_of_deckname = line.find('">',28)+2
			end_of_deckname = line.find('</a>')
			decklist.deckname = line[beginning_of_deckname:end_of_deckname]

		# If we find the name of the pilot, use that.
		if line[0:28] == '<header class="player_name">':
			beginning_of_pilot = line.find('">',29)+2
			end_of_pilot = line.find('</a>')
			decklist.pilot = line[beginning_of_pilot:end_of_pilot]

		# If we find the event line, use that too.
		if line.find('Place at <a href') != -1:
			end_of_place = line.find(' at <a href')
			decklistplace = line[:end_of_place]

			start_of_event = line.find('<a href')+11
			end_of_event = line.find('</a>')
			decklist.event = line[start_of_event:end_of_event]

			start_of_date = line.find('</a>')+8
			end_of_date = line.find(' </header')
			decklist.date = line[start_of_date:end_of_date]


		# Many cards appear on the same line. As a result, we will keep track of where we are in the line with the scanning_position.
		scanning_position = 1   

		while True:
			position_of_indicator = line.find('http://sales.starcitygames.com/cardsearch.php?singlesearch=', scanning_position) # This is what I am using as an indicator that we are talking about a card.
			if position_of_indicator == -1:	# In this case, there are no more cards on this line, so we can break and move on to the next line.
				break

			position_of_end_of_card = line.find('" rel=',position_of_indicator)		# We can find the end of the card with its quotation mark and such
			
			# We want to be able to read decklists that have two-digit numbers in them. So we have to find the starting <li>.
			position_of_start_of_number = 4 + line.find('<li>',position_of_indicator - 20)	
			if position_of_start_of_number == 3:	# If the <li> is actually at the start of the line, we will get a -1; in this case just set the start of the number to be at position 4.
				position_of_start_of_number = 4

			digits_in_the_number = position_of_indicator - position_of_start_of_number - 10		# The further apart the start_of_number and the indicator, the more digits the number has.

			# Now we can just grab the card name and the number.
			cardname = line[position_of_indicator + 59:position_of_end_of_card]		
			number = line[position_of_start_of_number:position_of_start_of_number + digits_in_the_number]

			if maindeck_flag:
				decklist.addmaindeckcard(cardname, number)
			else:
				decklist.addsideboardcard(cardname, number)

			# Now move on beyond the previous indicator to see if there are more cards on this line.
			scanning_position = position_of_indicator + 1	
	
	return decklist





def getDeckDirectory():

	# Go see how many decks we have available.
	deckdirectory = os.listdir( 'decks/' )
	numberofdecks = len(deckdirectory)

	if numberofdecks == 0:
		exit('You don\'t seem to have any decks in the /decks/ subdirectory. Download HTML decklists from starcity\'s website to get them.')

	return deckdirectory








if __name__ == "__main__":

	deckdirectory = getDeckDirectory()
	listofDecklists = []

	# Go through and parse all the decklists in the folder.
	for (i, deckfile) in enumerate(deckdirectory):
		decklist = parseDecklist(deckfile)
		listofDecklists.append(decklist)

	# Now find which cards are actually mentioned, keeping track of how often they are mentioned.
	cards = {}
	for decklist in listofDecklists:
		for card in decklist.maindeck.keys():
			if card not in cards: 
				cards[card] = decklist.maindeck[card]
			else:
				cards[card] += decklist.maindeck[card]
		for card in decklist.sideboard.keys():
			if card not in cards: 
				cards[card] = decklist.sideboard[card]
			else:
				cards[card] += decklist.sideboard[card]
	
	# Print the average decklist.
	for card in sorted(cards, key=cards.__getitem__, reverse=True):
		print(str(round(cards[card]/len(deckdirectory))) + ' ' + card)


	# Now let's do a distance matrix.
	maxmatrixsize = 1000
	matrix = []
	for (i, decklist1) in enumerate(listofDecklists):
		if i < maxmatrixsize:
			# print(decklist1)
			row = []
			for (j, decklist2) in enumerate(listofDecklists):
				if j < maxmatrixsize:
					row.append(distance(decklist1, decklist2))
			matrix.append(row)
