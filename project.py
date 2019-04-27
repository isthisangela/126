import random
import networkx as nx 
import numpy as np
from scipy.integrate import quad

class Node:
	""" 
	A Node represents a person in a graph, should have the following:
	-a randomized lambda value for each person for which we plug into the pdf of an exponential function (between 0.0666, 0.5)
	-a level of wealth (0 to 1)
	-an int value in (0, 1, 2) representing status for whether someone is uninvolved, involved, or out
	"""

	def __init__(self):

		# randomize the lambda, wealth, and closeness

		self.goat = random.uniform(0.0666, 0.5)
		self.wealth = random.uniform(0.001, 1)
		self.status = 0 # uninvolved
		self.patience = self.wealth * 1/(random.uniform(0.00001, 0.001))
		# wealth * some scalar = patience, how many time steps they wait iuntil sending another invite
		self.sent_invites = 0  # how many people theyve sent invites to
		self.accepted = 0 # 
		self.start_time = -1
		# 0 = cashed out/got money, 1 = lost money/failed, 2 = declined
		self.gained_money = -1

	#lower bounded by 0
	def get_probability(self, lower, upper):
		return quad(self.exp_pdf, lower, upper)[0]

	def exp_pdf(self, x):
		return self.goat * np.exp(-1 * self.goat * x)

# node = Node()
# i = 0
# while node.get_probability(0, i) < 0.93:
# 	i += 1

# print(i)

class Scheme:
	def __init__(self, threshold, money_to_join, num_recruits):
		self.threshold = threshold
		self.money_to_join = money_to_join
		self.num_recruits = num_recruits

# OUTPUT: (graph, fat_map): fat_map maps nodes to created nodes cuz can't generate graph with custom nodes
# can also generate based on probability?
# total number of people, edges

	def generate_graph(num_people, num_edges):
		graph = nx.gnm_random_graph(num_people, num_edges)
		for (u, v, w) in graph.edges(data = True):
	    	w["weight"] = random.uniform(0.001, 1)

	    fat_map = {}
	    for i in graph.nodes:
	    	fat_map[i] = Node()

	    self.graph = graph
	    self.fat_map = fat_map
	    self.time = 0
	    self.curr_involved = []
	    self.curr_invited = {}
	    self.uninvolved = graph.nodes

	# graph, fat_map, curr time step, people in the scheme rn, people who haven't been involved yet
	def increment_time():
		if not len(self.uninvolved):
			print("but we done boi")
			return
		#find a person to start (no one currently involved)
		while not self.curr_involved:
			rando = random.randint(0, len(self.uninvolved))
			start = self.uninvolved.pop(rando)
			if not self.graph.degree[start]:
				self.fat_map[start].status = 2
				self.fat_map[start].gained_money = 2
			else:
				#JK just don't include them
				if len(self.graph.adj[start]) < self.num_recruits:
					self.uninvolved.append(start)
				else:
					#yes
					add_involved(start)

		# when someone is done/cashed out, i remove the node in inviter
		for inviter in curr_invited:
			for invited in curr_invited[inviter]:
				inviter_node = self.fat_map[inviter]
				invited_node = self.fat_map[invited]
				offset = self.time - invited_node.start_time
				response = invited_node.get_probability(0, offset)
				#random threshold for responding
				if response > 0.93:
					answer = (1/self.graph[inviter][invited]["weight"]) * invited_node.wealth
					#accept
					if answer >= self.threshold:
						add_involved(invited)
						self.curr_invited[inviter].remove(invited)
						inviter_node.accepted += 1
						if inviter_node.accepted == self.num_recruits:
							inviter_node.status = 2
							inviter_node.gained_money = 0
							remove_involved(inviter)
							break
					#decline
					else:

		for person in self.curr_involved:
			# they out of the scheme
			if len(self.graph[person]) < self.num_recruits: # not enough friends
				self.fat_map[person].status = 2
				self.fat_map[person].gained_money = 1
				self.curr_involved.remove(person)

			#sort neighbors by edge weight largest to smallest
			neighbors = sorted(self.graph.adj[person], key = lambda x: self.graph[person][x]["weight"], reverse = True)

			#send invites to first num_recruits closest friends
			# need to make sure they are not out or have denied
			for index in range(num_recruits):
				self.curr_invited.add(neighbors[index])
				self.fat_map[person].sent_invites += 1 # 

	def add_involved(person):
		node = self.fat_map[person]
		self.uninvolved.remove(person)
		self.curr_involved.append(person)
		self.curr_invited[person] = []
		node.status = 1
		node.start_time = self.time

	#modify status and gained_money outside of function
	def remove_involved(person):
		node = self.fat_map[person]
		self.curr_involved.remove(person)
		del self.curr_invited[person]

