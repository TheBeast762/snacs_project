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
from numba import cuda 

def readNetwork(filename):
	return ig.Graph.Read_Ncol(open(filename), names=False, weights="if_present", directed=True)

def leafPrune(graph):#{leafNode, Connection}
  nodeDeg = dict(zip([vertex.index for vertex in graph.vs], graph.degree(graph.vs)))#{node: degree}
  leafNodes = [k for k,v in nodeDeg.items() if v == 1]#all nodes degree 1
  leafConnections = [edge.tuple for edge in graph.es.select(_incident=leafNodes)]#all edges connected to leaf nodes #leafEdgeData.attributes() if applicable
  graph.delete_edges(leafConnections)
  return leafNodes, leafConnections

def leafAdd(graph, partition, leafConnections, leafNodes):
  graph.add_edges(leafConnections)#reconnect edges to graph
  partition = louvain.ModularityVertexPartition(graph, initial_membership=partition._membership)#make new partition with reconnected edges, with computed partition
  for leafEdge in leafConnections:
    if leafEdge[0] in leafNodes:#leaf is source node
      [community] = [index for index, comm in enumerate(partition) if leafEdge[1] in comm]
      leaf = leafEdge[0]
    else:#leaf is target node
      [community] = [index for index, comm in enumerate(partition) if leafEdge[0] in comm]
      leaf = leafEdge[1]
    #print(leafEdge, " ", partition.diff_move(leaf, community))
    #if partition.diff_move(leaf, community) > 0:
    partition.move_node(leaf, community)
  partition.renumber_communities()
  return partition

@cuda.jit()
def performExperiment(G, threshold, comm_select, leafExclude):
	t_start = time.time()
	part = louvain.find_partition(G, louvain.ModularityVertexPartition, threshold=threshold, comm_select=comm_select)
	t_end = time.time()
	if leafExclude:
		leafAdd(G, part, leafConnections, leaves)
	return part.quality(), (t_end-t_start)

if __name__ == "__main__":
	#Community Select methods:
	# 1 = ALL_COMMS (baseline Louvain)
	# 2 = ALL_NEIGH_COMMS 
	# 3 = RAND_COMM
	# 4 = RAND_NEIGH_COMM (Traag's Improved Method)
	G = readNetwork("medium.tsv")
	settings_list = [(0.0, 1, False), (0.01, 1, False)]
	for setting in settings_list:
		print("______________________________")
		print("LeafNodeExclusion used?: ", leafExclude)
		if setting[2]:
			leaves, leafConnections = leafPrune(G)
		print(performExperiment(G, setting[0], setting[1], setting[2]))