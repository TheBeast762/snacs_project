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
import numpy as np

def readNetwork(filename, directed=True):
	print("reading {}...".format(filename))
	return ig.Graph.Read_Ncol(open(filename), names=False, weights="if_present", directed=directed)

def leafPrune(graph):#{leafNode, Connection}
  leafNodes = [v.index for v in graph.vs.select(_degree_eq=1)]#all nodes degree 1
  leafSources = [edge.tuple for edge in graph.es.select(_source_in=leafNodes)]#all edges connected to leaf nodes #leafEdgeData.attributes() if applicable
  leafTargets = [edge.tuple for edge in graph.es.select(_target_in=leafNodes)]
  graph.delete_edges(leafSources + leafTargets)
  return leafSources, leafTargets, len(leafNodes)

def leafAdd(graph, partition, leafSources, leafTargets):
	t_start = time.time()
	graph.add_edges(leafSources + leafTargets)#reconnect edges to graph
	partition = louvain.ModularityVertexPartition(graph, initial_membership=partition._membership)
	for edge in leafSources:
		partition.move_node(edge[0], partition._membership[edge[1]])
	for edge in leafTargets:
		partition.move_node(edge[1], partition._membership[edge[0]])
	t_end = time.time()
	print("LeafAdd duration: ", t_end-t_start)
	partition.renumber_communities()
	return partition, (t_end-t_start)

def performExperiment(G, threshold, comm_select, leafExclude, q, t, leafTime):
	leafTime = 0.0
	print("Full network size: ", G.vcount(), G.ecount())
	if leafExclude:
		leafSources, leafTargets, nLeaves = leafPrune(G)
		print("Pruned network size: ", G.ecount())
		print("----- {} leafNodes found in the Network-----".format(nLeaves))
		t_start = time.time()
		part = louvain.find_partition(G, louvain.ModularityVertexPartition, threshold=threshold, comm_select=comm_select)
		part, leafTime = leafAdd(G, part, leafSources, leafTargets)
		t_end = time.time()
		q = part.quality()
		t = (t_end-t_start)
	else: 
		t_start = time.time()
		part = louvain.find_partition(G, louvain.ModularityVertexPartition, threshold=threshold, comm_select=comm_select)
		t_end = time.time()
		q = part.quality() 
		t = (t_end-t_start)

if __name__ == "__main__":
	#Community Select methods:
	# 1 = ALL_COMMS (baseline Louvain)
	# 2 = ALL_NEIGH_COMMS 
	# 3 = RAND_COMM
	# 4 = RAND_NEIGH_COMM (Traag's Improved Method)
	method_dict = {1: "ALL_COMMS", 2: "ALL_NEIGH_COMMS", 3: "RAND_COMM", 4:"RAND_NEIGH_COMM"}
	settings_list = [(0.0, 1, False), (0.0, 2, False), (0.0, 3, False), (0.0, 4, False)]
	networks = [readNetwork("rec-amazon.tsv", False), readNetwork("soc-academia.tsv"), readNetwork("rt-higgs.tsv"), readNetwork("webbase-1M.tsv"), readNetwork("inf-netherlands_osm.tsv", False), readNetwork("venturiLevel3.tsv", False), readNetwork("DIMACS10.tsv", directed=False)]
	n_settings = len(settings_list)
	ind = np.arange(len(networks))
	q_dict = {}
	t_dict = {}
	network_sizes = []
	nLeaves = []

	for network in networks:#within 2 hours, if no result, cancel run
		network_size = network.vcount()
		network_sizes.append(network_size)
		for setting in settings_list:
			print("________________________________________")
			print("LNE used?: ", setting[2])
			q, t, leafTime = performExperiment(network, setting[0], setting[1], setting[2])
			print(q,t)
			if setting in q_dict:
				q_dict[setting].append(q)
				t_dict[setting].append((t, leafTime))
			else:
				q_dict[setting] = [q]
				t_dict[setting] = [(t, leafTime)]
	
	print("Start plotting...")
	print(q_dict)
	print(t_dict)
	print(nLeaves)
	print(network_sizes)

	
