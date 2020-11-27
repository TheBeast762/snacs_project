import matplotlib.pyplot as plt
import numpy as np
#EARLY FIRST PHASE STOPPING
#Three seperate graphs for three networks: 200K 400K 1M

q_dict = {(0.0, 2, False): [0.9898551500822698, 0.6589962686147389, 0.6094325995349, 0.9957565875742763, 0.8127030819321565], (0.0, 2, True): [0.9898845627727709, 0.6634072374381076, 0.6001319776503384, 0.995741405451887, 0.8112625968041698]}
t_dict = {(0.0, 2, False): [(1.0813076496124268, 0.0), (12.763123989105225, 0.0), (7.796864748001099, 0.0), (46.68864059448242, 0.0), (950.0833930969238, 0.0)], (0.0, 2, True): [(0.9944767951965332, 0.05438375473022461), (13.011586904525757, 0.30637598037719727), (7.959274530410767, 0.44858241081237793), (47.42874836921692, 0.9163942337036133), (677.6936872005463, 7.562430143356323)]}
network_sizes = [91813, 200169, 425008, 2216688, 3774768]
nLeaves = [19580, 18113, 282735, 129231, 667336]

ind = np.arange(len(network_sizes))
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
ax.set_yscale("log")
plt.ylabel("Time (s)")

ax.legend(bars, ["LNE:{}".format(setting[2]) for setting in t_dict.keys()])
plt.savefig('timeLNEPlot.png')