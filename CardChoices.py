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
		self.date = datetime.date(2000,1,1)
		self.event = ''
		self.pilot = ''
		self.maindeck = {}
		self.sideboard = {}

	def __repr__(self):
		outputString = 'Main deck: \n'
		for cardname in self.maindeck:
			outputString = outputString + self.maindeck[cardname] + 'x ' + cardname + '\n'
		outputString = outputString + 'Sideboard: \n'
		for cardname in self.sideboard:
			outputString = outputString + self.sideboard[cardname] + 'x ' + cardname + '\n'
		return outputString

	def addmaindeckcard(self, cardname, number):
		self.maindeck[cardname] = number
		return True

	def addsideboardcard(self, cardname, number):
		self.sideboard[cardname] = number
		return True



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


	print(decklist)		
	
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

	for (i, deckfile) in enumerate(deckdirectory):
		print(deckfile)
		decklist = parseDecklist(deckfile)
		break