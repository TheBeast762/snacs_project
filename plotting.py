import matplotlib.pyplot as plt
#EARLY FIRST PHASE STOPPING
#Three seperate graphs for three networks: 200K 400K 1M

q_dict = {(0.0, 2, False): [0.664274369167744, 0.609706338333967, 0.9626507565770311], (0.01, 2, False): [0.6624664903204937, 0.6059223150256585, 0.9625834318386112], (0.02, 2, False): [0.6585061112911649, 0.6065001635998495, 0.9626992291064914], (0.03, 2, False): [0.6642986876951537, 0.6069230022596434, 0.9626387964204636], (0.04, 2, False): [0.662836956893722, 0.6058796152824413, 0.9625818096739487], (0.05, 2, False): [0.6636757909504106, 0.6072639346186877, 0.9625848960391381], (0.06, 2, False): [0.6628811103616232, 0.6079656362891543, 0.9625880244215559], (0.07, 2, False): [0.6614476697896525, 0.5888384459039913, 0.9626541466090143], (0.08, 2, False): [0.6653722607194607, 0.5945230235523605, 0.9625100045580267], (0.09, 2, False): [0.6628941966845214, 0.5954134530662425, 0.9621472468410864], (0.1, 2, False): [0.6598739400774686, 0.5924947900069386, 0.956967690471016], (0.11, 2, False): [0.647773658873255, 0.5917979305965572, 0.9574092782630494], (0.12, 2, False): [0.6492064634278174, 0.5933057926997733, 0.9568854558999342], (0.13, 2, False): [0.647480560086069, 0.5943381992336148, 0.9572490460956612], (0.14, 2, False): [0.6496394176825461, 0.5919122195710844, 0.9569767835372166], (0.15, 2, False): [0.6443130187310806, 0.5933760744999782, 0.9573796886073239]}
t_dict = {(0.0, 2, False): [(10.565017700195312, 0.0), (7.673086881637573, 0.0), (46.73938798904419, 0.0)], (0.01, 2, False): [(14.981658220291138, 0.0), (6.82330846786499, 0.0), (46.1187539100647, 0.0)], (0.02, 2, False): [(12.549890279769897, 0.0), (6.462879180908203, 0.0), (38.82014465332031, 0.0)], (0.03, 2, False): [(13.70630407333374, 0.0), (7.616156578063965, 0.0), (45.04060983657837, 0.0)], (0.04, 2, False): [(12.742563724517822, 0.0), (7.6597654819488525, 0.0), (43.78149771690369, 0.0)], (0.05, 2, False): [(19.634793281555176, 0.0), (6.259188652038574, 0.0), (41.252485036849976, 0.0)], (0.06, 2, False): [(9.730854749679565, 0.0), (7.1127471923828125, 0.0), (46.67572474479675, 0.0)], (0.07, 2, False): [(11.243264436721802, 0.0), (6.5514609813690186, 0.0), (46.656609296798706, 0.0)], (0.08, 2, False): [(12.486989974975586, 0.0), (5.802687406539917, 0.0), (51.65561652183533, 0.0)], (0.09, 2, False): [(11.078082799911499, 0.0), (7.027929782867432, 0.0), (45.22061371803284, 0.0)], (0.1, 2, False): [(13.550190687179565, 0.0), (5.615347146987915, 0.0), (43.63991141319275, 0.0)], (0.11, 2, False): [(11.382856845855713, 0.0), (5.787895679473877, 0.0), (43.672186613082886, 0.0)], (0.12, 2, False): [(11.727290868759155, 0.0), (6.185527563095093, 0.0), (46.06031322479248, 0.0)], (0.13, 2, False): [(17.99031090736389, 0.0), (7.46021842956543, 0.0), (45.0110342502594, 0.0)], (0.14, 2, False): [(14.714779376983643, 0.0), (6.0804595947265625, 0.0), (46.71090483665466, 0.0)], (0.15, 2, False): [(13.208406925201416, 0.0), (5.779668092727661, 0.0), (42.43302273750305, 0.0)]}

τ = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15]

for ix, network in enumerate(['Academia Social Network', 'Twitter Retweet Subgraph', 'Webbase-2008']):
	fig, ax1 = plt.subplots()
	color = 'tab:red'
	ax1.set_xlabel('τ')
	ax1.set_ylabel('Q', color=color)
	ax1.plot(τ, [val[ix] for val in q_dict.values()], color=color)
	ax1.scatter(τ, [val[ix] for val in q_dict.values()], color=color)
	ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()  
	color = 'tab:blue'
	ax2.set_ylabel('Time (s)', color=color)  
	ax2.plot(τ, [val[ix][0] for val in t_dict.values()], color=color)
	ax2.scatter(τ, [val[ix][0] for val in t_dict.values()], color=color)
	ax2.tick_params(axis='y', labelcolor=color)

	plt.title(network)#TODO
	plt.savefig(network + '.png')