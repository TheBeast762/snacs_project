import matplotlib.pyplot as plt
#Method Comparison

q_dict = {(0.0, 2, False): [0.9898551500822698, 0.6589962686147389, 0.6094325995349, 0.9628487792392265, 0.9957565875742763, 0.8116072185134056, 0.9901550459406823], (0.0, 4, False): [0.9898068621848108, 0.6616985791624438, 0.6041595429602374, 0.962293321388465, 0.9956181493590542, 0.8104383330041143, 0.9895666331168518]}#setting: [q, q, ...]
t_dict = {(0.0, 2, False): [(1.1672277450561523, 0.0), (12.580533742904663, 0.0), (7.795973539352417, 0.0), (37.41572904586792, 0.0), (46.25916409492493, 0.0), (638.571994304657, 0.0), (244.62014198303223, 0.0)], (0.0, 4, False): [(2.3319756984710693, 0.0), (51.354244232177734, 0.0), (34.72269630432129, 0.0), (106.65697836875916, 0.0), (95.96523880958557, 0.0), (2330.1780834198, 0.0), (595.1327300071716, 0.0)]}#setting: [(t, leafTime), (t, leafTime), ...]
network_sizes = [91813, 200169, 425008, 1000005, 2216688, 3774768, 4194301]
nLeaves = [19580, 18113, 282735, 0, 129231, 667336, 54]
method_dict = {1: "ALL_COMMS", 2: "ALL_NEIGH_COMMS", 3: "RAND_COMM", 4:"RAND_NEIGH_COMM"}

#Plot Modularity
fig, ax1 = plt.subplots()
ax1.set_xlabel('n')
ax1.set_ylabel('Q')
ax1.set_yscale("log")
for _, val in q_dict.items():
	ax1.plot(network_sizes, val)
	ax1.scatter(network_sizes, val)
ax1.legend([method_dict[setting[1]] for setting in q_dict.keys()])#

plt.title("Community Select Method Q")
plt.savefig('methodModularity.png')


#Plot Time (s)
fig, ax1 = plt.subplots()
ax1.set_xlabel('n')
ax1.set_ylabel('Time (s)')
ax1.set_yscale("log")
for _, val in t_dict.items():
	ax1.plot(network_sizes, [tup[0] for tup in val])
	ax1.scatter(network_sizes, [tup[0] for tup in val])
ax1.legend([method_dict[setting[1]] for setting in q_dict.keys()])#

plt.title("Community Select Method Time (s)")
plt.savefig('methodTime.png')