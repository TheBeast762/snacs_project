import louvain
import igraph as ig

G = ig.Graph.Erdos_Renyi(100, 0.04)
part = louvain.find_partition(G, louvain.ModularityVertexPartition, 0.01, comm_select=4)
print(part)