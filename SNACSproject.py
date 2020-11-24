#ssh s1853767@sshgw.leidenuniv.nl
#ssh huisuil01.vuw.leidenuniv.nl
#ssh -K U0032504
#git clone https://github.com/TheBeast762/snacs_project.git
#/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
#brew install autoconf
#brew install automake
#brew install flex
#brew install bison
#brew install igraph
#cd /vol/home/s1853767/miniconda3/compiler_compat
#mv ld ld-old
#python3 setup.py --use-pkg-config build
#python3 setup.py --use-pkg-config install
import louvain
import igraph as ig
import time 
import matplotlib.pyplot as plt

def readNetwork(filename, directed=True):
	print("reading {}...".format(filename))
	return ig.Graph.Read_Ncol(open(filename), names=False, weights="if_present", directed=directed)

def leafPrune(graph):#{leafNode, Connection}
	leafNodes = [v.index for v in graph.vs.select(_degree_lt=2)]#all nodes degree 0-1
	if len(leafNodes) == 0:
		return [], []
	return leafNodes, graph.subgraph(vertices=graph.vs.select(_degree_gt=1))

def leafAdd(graph, partition, leafNodes):
	if not leafNodes:
		return partition
	n_comm = len(partition._membership)
	for leaf in leafNodes:
		partition._membership.insert(leaf, n_comm)
		n_comm += 1

	part = louvain.ModularityVertexPartition(graph, initial_membership=partition._membership)
	leafSources = [edge.tuple for edge in graph.es.select(_source_in=leafNodes)]#all edges connected to leaf nodes #leafEdgeData.attributes() if applicable
	leafTargets = [edge.tuple for edge in graph.es.select(_target_in=leafNodes)]
	for edge in leafSources:
		part.move_node(edge[0], partition._membership[edge[1]])
	for edge in leafTargets:
		part.move_node(edge[1], partition._membership[edge[0]])
	part.renumber_communities()
	return part

def performExperiment(G, threshold, comm_select, leafExclude):
	print("Full network size: ", G.vcount(), G.ecount())
	if leafExclude:
		leaves, subGraph = leafPrune(G)
		print("----- {} leafNodes found in the Network-----".format(len(leaves)))
		print("Pruned network size: ", subGraph.vcount(), subGraph.ecount())
		t_start = time.time()
		part = louvain.find_partition(subGraph, louvain.ModularityVertexPartition, threshold=threshold, comm_select=comm_select)
		part = leafAdd(G, part, leaves)
		t_end = time.time()
		return part.quality(), (t_end-t_start), len(leaves)
	else: 
		t_start = time.time()
		part = louvain.find_partition(G, louvain.ModularityVertexPartition, threshold=threshold, comm_select=comm_select)
		t_end = time.time()
	return part.quality(), (t_end-t_start), 0

if __name__ == "__main__":
	#Community Select methods:
	# 1 = ALL_COMMS (baseline Louvain)
	# 2 = ALL_NEIGH_COMMS 
	# 3 = RAND_COMM
	# 4 = RAND_NEIGH_COMM (Traag's Improved Method)
	method_dict = {1: "ALL_COMMS", 2: "ALL_NEIGH_COMMS", 3: "RAND_COMM", 4:"RAND_NEIGH_COMM"}
	settings_list = [(0.0, 1, False), (0.0, 1, True), (0.0, 2, False), (0.0, 2, True), (0.0, 3, False), (0.0, 3, True), (0.0, 4, False), (0.0, 4, True)]#threshold, comm_select, leaf_node_exclusion
	networks = [readNetwork("rec-amazon.tsv"), readNetwork("soc-academia.tsv"), readNetwork("rt-higgs.tsv"), readNetwork("inf-roadNet-PA.tsv"), readNetwork("inf-netherlands_osm.tsv", False)]#
	q_dict = {}
	t_dict = {}
	leaves_amount = []
	network_sizes = []
	nLeaves = 0

	for network in networks:
		network_size = network.vcount()
		network_sizes.append(network_size)
		for setting in settings_list:
			print("________________________________________")
			print("LeafNodeExclusion used?: ", setting[2])
			q, t, nLeaves = performExperiment(network, setting[0], setting[1], setting[2])
			print(q,t)
			if setting in q_dict:
				q_dict[setting].append((network_size, q))
				t_dict[setting].append((network_size, t))
			else:
				q_dict[setting] = [(network_size, q)]
				t_dict[setting] = [(network_size, t)]
		leaves_amount.append(nLeaves)
	
	print(q_dict)
	print(t_dict)
	print("Start plotting...")
	f, ax = plt.subplots(figsize=(10,8))
	for key, val in q_dict.items():#setting: [network_size, modularity]
		x,y = zip(*val)
		plt.plot(x,y)
		plt.scatter(x,y)
	plt.xlabel("n")
	ax.set_xscale('log')
	plt.ylabel("Q")
	ax.legend(["{}, LNE:{}".format(method_dict[setting[1]],setting[2]) for setting in q_dict.keys()])
	plt.savefig('modularityPlot.png')

	f, ax = plt.subplots(figsize=(10,8))
	for key, val in t_dict.items():#setting: [network_size, modularity]
		x,y = zip(*val)
		plt.plot(x,y)
		plt.scatter(x,y)
	plt.xlabel("n")
	ax.set_xscale('log')
	plt.ylabel("Time (s)")
	ax.legend(["{}, LNE:{}".format(method_dict[setting[1]],setting[2]) for setting in t_dict.keys()])
	plt.savefig('timePlot.png')