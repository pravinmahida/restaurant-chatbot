from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
import zomatopy
import json

from city_check import check_location
from email_config import Config
from flask_mail_check import send_email
from zomato_res_search import restaurant_search




class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_restaurant'
		
	def run(self, dispatcher, tracker, domain):
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		price = tracker.get_slot('price')

		global restaurants

		restaurants = restaurant_search(loc, cuisine, price)
		top5 = restaurants.head(5) 
		
		# top 5 results to display
		if len(top5)>0:
			response = 'Showing you top results:' + "\n"
			for index, row in top5.iterrows():
				response = response + str(row["restaurant_name"]) + ' (rated ' + row['restaurant_rating'] + ') in ' + row['restaurant_address'] + ' and the average budget for two people ' + str(row['budget_for2people'])+"\n"
				response = response + "\nShould i mail you the details"

		else:
			response = 'No restaurants found' 

		dispatcher.utter_message(str(response))



class SendMail(Action):
	def name(self):
		return 'email_restaurant_details'
		
	def run(self, dispatcher, tracker, domain):
		recipient = tracker.get_slot('email')

		top10 = restaurants.head(10)
		print("got this correct email is {}".format(recipient))
		send_email(recipient, top10)

		dispatcher.utter_message("Have a great day!")


class Check_location(Action):
	def name(self):
		return 'action_check_location'
		
	def run(self, dispatcher, tracker, domain):
		loc = tracker.get_slot('location')
		check = check_location(loc)
		
		return [SlotSet('location',check['location_new']), SlotSet('location_found',check['location_f'])]
		
		
