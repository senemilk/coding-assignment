#!usr/bin/python
# -*- coding: utf-8 -*-


class Database(object):

	def __init__(self, core):
		self.extract = dict()
		self.status = dict()
		self.state_node = dict()
		if (type(core) == str):
			self.graph = [(core, None)]
			#self.state_node[core] = "new"

	def add_nodes(self, nodes):
		i=0
		graph_list = [item for t in self.graph for item in t]
		for i in range(len(nodes)):
			self.graph.append(nodes[i])
			if nodes[i][0] not in graph_list:
				self.state_node[nodes[i][0]] = "new"
			if nodes[i][1] not in graph_list:
				self.state_node[nodes[i][1]] = "new"

	def add_extract(self, extract):
		graph_list = [item for t in self.graph for item in t]
		for i in extract:
			if extract[i] == [] :
				self.status[i] = "valid"
			else:
				for node in extract[i]:
					if node not in graph_list:
						self.status[i] = "invalid"
					else:
						self.status[i] = "valid"
			if i in self.extract: 
				self.extract[i].extend(extract[i])
			else:
				self.extract[i] = extract[i]
		for n in range(len(self.graph)) :
			self.state_node[self.graph[n][0]] = "old"
			self.state_node[self.graph[n][1]] = "old"

	def get_extract_status(self):
		for i in self.extract :
			if self.status[i] == "valid" :
				for node in self.extract[i]:
					neighbors = self.get_neighbors(node)
					children = self.get_children(node)
					for n in neighbors:
						if self.state_node[n] == "new":
							self.status[i] = "coverage_staged"
							break
					if self.status[i] == "coverage_staged":
						break
					for c in children :
						if self.state_node[c] == "new":
							self.status[i] = "granularity_staged"
							break
		return self.status
				
	def get_parent(self, node):
		n=0
		for n in range(len(self.graph)) :
			if self.graph[n][0] == node :
				parent = self.graph[n][1]
		return parent
				

	def get_neighbors(self, node):
		parent = self.get_parent(node)
		children = self.get_children(parent)
		children.remove(node)
		neighbors = children
		return neighbors


	def get_children(self, node):
		children = []
		for t in self.graph:
			if node == t[1]:
				children.append(t[0])
		return children


	def get_nodes(self):
		nodes = []
		for t in self.graph:
			if t[0] not in nodes:
				nodes.append(t[0])
		return nodes
