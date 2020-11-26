import matplotlib.pyplot as plt
#EARLY FIRST PHASE STOPPING
#Three seperate graphs for three networks: 200K 400K 1M

τ = [0.0, 0.01, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15]
q = [0.9892891672898281, 0.988553032506642, 0.9885750473719566, 0.9800843536121417, 0.9509213642863917, 0.950924075868179, 0.9505491788758539, 0.8818583763026049]
t = [23.12250328063965, 22.092003107070923, 23.617916584014893, 20.760008096694946, 21.883973836898804, 22.039660453796387, 21.43942379951477, 21.34670090675354]

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

plt.title("Pennsylvania Road Network")#TODO
plt.savefig('τqt.png')