import matplotlib.pyplot as plt
#EARLY FIRST PHASE STOPPING
#Three seperate graphs for three networks: 200K 400K 1M

q_dict = {(0.0, 2, False): [0.9898551500822698, 0.6589962686147389, 0.6094325995349, 0.9628487792392265, 0.9957565875742763, 0.9854458660634027], (0.0, 2, True): [0.9898845627727709, 0.6634072374381076, 0.6001319776503384, 0.9628182968307983, 0.995741405451887, 0.9855345436330497]}
t_dict = {(0.0, 2, False): [(1.0813076496124268, 0.0), (12.763123989105225, 0.0), (7.796864748001099, 0.0), (38.39695954322815, 0.0), (46.68864059448242, 0.0), (168.30146431922913, 0.0)], (0.0, 2, True): [(0.9944767951965332, 0.05438375473022461), (13.011586904525757, 0.30637598037719727), (7.959274530410767, 0.44858241081237793), (49.24335050582886, 0.47136473655700684), (47.42874836921692, 0.9163942337036133), (185.49560475349426, 1.7904839515686035)]}
network_sizes = [91813, 200169, 425008, 1000005, 2216688, 4026819]
nLeaves = [19580, 18113, 282735, 0, 129231, 0]

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