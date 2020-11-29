import matplotlib.pyplot as plt
#Method Comparison

q_dict = #setting: [q, q, ...]
t_dict = #setting: [(t, leafTime), (t, leafTime), ...]
network_sizes = [91813, 200169, 425008, 1000005, 2216688, 3774768, 4194301]
nLeaves = [19580, 18113, 282735, 0, 129231, 667336, 54]
method_dict = {1: "ALL_COMMS", 2: "ALL_NEIGH_COMMS", 3: "RAND_COMM", 4:"RAND_NEIGH_COMM"}

#Plot Modularity
fig, ax1 = plt.subplots()
ax1.set_xlabel('n')
ax1.set_ylabel('Q')
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
for _, val in t_dict.items():
	ax1.plot(network_sizes, val)
	ax1.scatter(network_sizes, val)
ax1.legend([method_dict[setting[1]] for setting in q_dict.keys()])#

plt.title("Community Select Method Time (s)")
plt.savefig('methodTime.png')