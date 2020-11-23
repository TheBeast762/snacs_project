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

def readNetwork(filename):
	print("reading {}...".format(filename))
	return ig.Graph.Read_Ncol(open(filename), names=False, weights="if_present", directed=True)

def leafPrune(graph):#{leafNode, Connection}
  leafNodes = [v.index for v in graph.vs.select(_degree_eq=1)]#all nodes degree 1
  if len(leafNodes) == 0:
  	return [], [], 0
  leafSources = [edge.tuple for edge in graph.es.select(_source_in=leafNodes)]#all edges connected to leaf nodes #leafEdgeData.attributes() if applicable
  leafTargets = [edge.tuple for edge in graph.es.select(_target_in=leafNodes)]
  graph.delete_edges(leafSources + leafTargets)
  return leafSources, leafTargets, len(leafNodes)

def leafAdd(graph, partition, leafSources, leafTargets):
	if len(leafSources) == 0 or len(leafTargets) == 0:
		return partition, 0.0
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

def performExperiment(G, threshold, comm_select, leafExclude):
	leafTime = 0.0
	print("Full network size: ", G.vcount(), G.ecount())
	if leafExclude:
		leafSources, leafTargets, nLeaves = leafPrune(G)
		print("----- {} leafNodes found in the Network-----".format(nLeaves))
		print("Pruned network size: ", G.ecount())
	t_start = time.time()
	part = louvain.find_partition(G, louvain.ModularityVertexPartition, threshold=threshold, comm_select=comm_select)
	t_end = time.time()
	if leafExclude:
		part, leafTime = leafAdd(G, part, leafSources, leafTargets)
		return part.quality(), (t_end-t_start+leafTime), nLeaves
	return part.quality(), (t_end-t_start+leafTime), 0

if __name__ == "__main__":
	#Community Select methods:
	# 1 = ALL_COMMS (baseline Louvain)
	# 2 = ALL_NEIGH_COMMS 
	# 3 = RAND_COMM
	# 4 = RAND_NEIGH_COMM (Traag's Improved Method)
	method_dict = {1: "ALL_COMMS", 2: "ALL_NEIGH_COMMS", 3: "RAND_COMM", 4:"RAND_NEIGH_COMM"}
	settings_list = [(0.0, 2, False), (0.0, 2, True), (0.0, 4, False), (0.0, 4, True)]#threshold, comm_select, leaf_node_exclusion
	networks = [readNetwork("medium.tsv")]#[readNetwork("rec-amazon.tsv"), readNetwork("soc-academia.tsv"), readNetwork("rt-higgs.tsv"), readNetwork("inf-roadNet-PA.tsv")]#100196, 125K, 200K, 425K, 1M
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
	
	t_dict = {(0.0, 2, False): [(91813, 1.1705708503723145), (200169, 12.926081657409668), (425008, 7.170727729797363), (1087562, 22.454992055892944)], (0.0, 2, True): [(91813, 0.9594748020172119), (200169, 15.115833282470703), (425008, 8.366578340530396), (1087562, 24.696043252944946)], (0.0, 4, False): [(91813, 2.2790768146514893), (200169, 50.753785371780396), (425008, 30.633625268936157), (1087562, 49.341519832611084)], (0.0, 4, True): [(91813, 1.8622634410858154), (200169, 66.05050611495972), (425008, 32.957130432128906), (1087562, 48.41746664047241)]}
	q_dict = {(0.0, 2, False): [(91813, 0.9898459304170207), (200169, 0.6632481776933347), (425008, 0.6100103264751499), (1087562, 0.9892106916645698)], (0.0, 2, True): [(91813, 0.9897899268575165), (200169, 0.6652775163385561), (425008, 0.6018685367052669), (1087562, 0.989148708141077)], (0.0, 4, False): [(91813, 0.9897894402580069), (200169, 0.665051947581073), (425008, 0.6048222738269), (1087562, 0.9886757498956593)], (0.0, 4, True): [(91813, 0.9897852217965646), (200169, 0.6623645703786281), (425008, 0.5956118844101304), (1087562, 0.9886554986818218)]}
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
	ax2 = ax.twinx()
	ax2.set_ylabel("Leaf Nodes")
	ax2.bar(x=network_sizes, width=0.1, height=leaves_amount, fc=(0, 0, 0, 0.1))
	ax.legend(["τ:{}, {}, LNE:{}".format(setting[0],method_dict[setting[1]],setting[2]) for setting in q_dict.keys()])
	plt.savefig('modularityPlot.png')

	f, ax = plt.subplots(figsize=(10,8))
	for key, val in t_dict.items():#setting: [network_size, modularity]
		x,y = zip(*val)
		plt.plot(x,y)
		plt.scatter(x,y)
	plt.xlabel("n")
	ax.set_xscale('log')
	plt.ylabel("Time (s)")
	ax2 = ax.twinx()
	ax2.set_ylabel("Leaf Nodes")
	ax2.bar(x=network_sizes, width=0.1 ,height=leaves_amount, fc=(0, 0, 0, 0.1))
	ax.legend(["τ:{}, {}, LNE:{}".format(setting[0],method_dict[setting[1]],setting[2]) for setting in t_dict.keys()])
	plt.savefig('timePlot.png')