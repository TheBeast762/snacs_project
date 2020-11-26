import matplotlib.pyplot as plt
#EARLY FIRST PHASE STOPPING
#Three seperate graphs for three networks: 200K 400K 1M

q_dict =  
t_dict = 
network_sizes = [2216688, ]

f, ax = plt.subplots(figsize=(10,8))
for ix, val in enumerate(q_dict.values()):#setting: [modularity]
	plt.bar(ind + ix*0.2, val, width = 0.2)
plt.xticks(ticks=range(len(network_sizes)), labels=network_sizes)#ticks param for x location
plt.xlabel("n")
plt.ylabel("Q")
ax.legend(["LNE:{}".format(setting[2]) for setting in q_dict.keys()])
plt.savefig('modularityLNEPlot.png')

f, ax = plt.subplots(figsize=(10,8))
bars = []
for ix, val in enumerate(t_dict.values()):#setting: [modularity]
	bars.append(plt.bar(ind + ix*0.2, [tup[0] for tup in val], width = 0.2))
	plt.bar(ind + ix*0.2, [tup[1] for tup in val], width = 0.2, bottom=[tup[0] for tup in val], color='b')
plt.xticks(ticks=range(len(network_sizes)), labels=network_sizes)
plt.xlabel("n")
plt.ylabel("Time (s)")
ax.legend(bars, ["LNE:{}".format(setting[2]) for setting in t_dict.keys()])
plt.savefig('timeLNEPlot.png')