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


class Decklist:
	# A decklist is a dictionary of cards in the maindeck and a dictionary of cards in the sideboard.

	def __init__(self):
		self.date = datetime.date(2000,1,1)
		self.
		self.maindeck = {}
		self.sideboard = {}

	def addmaindeckcard(self, cardname, number):
		self.maindeck[cardname] = number
		return True

	def addsideboardcard(self, cardname, number):
		self.sideboard[cardname] = number
		return True



def parseDecklist(filename):
	# We need to read through the HTML file from starcity and grab the amounts of each card.
	return True









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
		decklist = parsedecklist(deckfile)