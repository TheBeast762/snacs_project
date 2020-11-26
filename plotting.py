import numpy as np
import matplotlib.pyplot as plt
#EARLY FIRST PHASE STOPPING
#Three seperate graphs for three networks: 200K 400K 1M

τ = [0.0, 0.01, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15]
q = [1, 2, 3, 4, 5, 6, 7, 8]#TODO
t = [8, 7, 6, 5, 4, 3, 2, 1]#TODO


fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_xlabel('τ')
ax1.set_ylabel('Q', color=color)
ax1.plot(τ, q, color=color)
ax1.scatter(τ, q, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  
color = 'tab:blue'
ax2.set_ylabel('Time (s)', color=color)  
ax2.plot(τ, t, color=color)
ax2.scatter(τ, t, color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.title("Academia online social network")#TODO
plt.savefig('τqt.png')