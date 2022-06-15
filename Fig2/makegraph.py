#!/usr/local/bin/python

import warnings
warnings.filterwarnings('ignore', 'Could not import the lzma module.')
import itertools
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import networkx as nx
import sys
import cPickle as pickle
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


iters = 1000
cmap_name = 'hsv'
file_mat = 'full-set/22-inter-cluster.mat'
file_cluster = 'full-set/22-clustered.txt'

#file_mat = sys.argv[1]
#file_cluster = sys.argv[2]


# write coord dataframe to file
def write_positions(fd, pos_d):
	#pos_d.
	pos_d.to_csv(fd)


#  coord dataframe to file
def read_positions(fd):
	df = pd.read_csv(fd, index_col=0)
	return df


# convert dataframe to dictionary
def to_dict(pos_d):
	return pos_d.transpose().to_dict('list')


# load the positions into the dataframe
def load_positions(pos):
	pos_d = pd.DataFrame(pos).transpose()
	pos_d = pos_d.rename(columns={0:'x', 1:'y'})
	pos_d.index = pos_d.index.rename('cluster_id')
	return pos_d


# initialize the plot
def initialize_plot():
	plt.figure(figsize=(10,7.5))


# save the plot
def save_plot(fd):
	plt.tick_params(left=True, labelleft=True, bottom=True, \
		labelbottom=True)
	#plt.grid()
	plt.xlim((-1.2,1.2))
	plt.ylim((-1.2,1.2))
	plt.savefig(fd,dpi=600)
	plt.close()


# plot nodes
def plot_positions(pos, cluster_d, graph, scale=300, \
	           node_colors='#000000', node_alphas=0.2, lower=10,
                   edge_colors='#000000'):

	# calculate frequency
	freqs = cluster_d['cluster_id'].value_counts(sort=False) \
		.sort_index()
	freqs = freqs/max(freqs)*scale
	node_sizes = freqs
	node_sizes = freqs.clip(lower=lower)


	# make the plot
        fig, ax = plt.subplots(figsize=(6.4,6.4))
        ax.axis('off')
	nx.draw_networkx_nodes(graph, pos, alpha=node_alphas, \
		               node_size=node_sizes, node_color=node_colors,\
                               edgecolors=edge_colors)
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

# plot edges
def plot_edges(pos, graph, edge_min=24.0, edge_max=40.0, edge_alphas=0.1):
        graph = graph.copy()

        cmap = plt.get_cmap(cmap_name)
        new_cmap = cmap(np.linspace(0,1,1000))

        o = 0.0

        for i in xrange(1000):
                new_cmap[i][0] += o
                if new_cmap[i][0] > 1:
                        new_cmap[i][0] = 1
                new_cmap[i][1] += o
                if new_cmap[i][1] > 1:
                        new_cmap[i][1] = 1
                new_cmap[i][2] += o
                if new_cmap[i][2] > 1:
                        new_cmap[i][2] = 1

        
        new_cmap = ListedColormap(new_cmap)

        # only show edges above the threshold
        edge_list = [e for e in graph.edges.data('weight') \
                if e[2] > edge_min]
        edge_weights = [e[2] for e in edge_list]

        #e = nx.draw_networkx_edges(graph, pos, edgelist=edge_list, \
                #edge_color=edge_weights, alpha=edge_alphas, \
                               #edge_cmap=cmap, \
                               #edge_vmin=edge_min, \
                #edge_vmax=edge_max)

        #plt.colorbar(e)

        e = nx.draw_networkx_edges(graph, pos, edgelist=edge_list, \
                                   edge_color='#AAAAAA', alpha=edge_alphas, \
                                   edge_vmin=edge_min, \
                                   edge_vmax=edge_max)

        return new_cmap


# plot labels
def plot_labels(pos, graph, font_size=6):
        labels = {i: i for i in graph.nodes}
        nx.draw_networkx_labels(graph, pos, labels, font_size=font_size)


# plot colorbar
def plot_colorbar(cbar, edge_min=22.0, edge_max=40.0):
        #plt.colorbar(matplotlib.cm.ScalarMappable( \
                #matplotlib.colors.Normalize(edge_min, edge_max), \
                                                   #cbar))
        #plt.colorbar([0.22,0.4],cbar)
        plt.colorbar()



# INSTANCE-SPECIFIC FUNCTIONS
# highlight nodes (not specific)
def highlight_nodes():
        node_colors = ['#000000' for i in range(len(mat))]
        node_colors[76] = '#6F286B' # KNusG
        node_colors[79] = '#0D7943' # TRfaH
        node_colors[243] = '#FC7802' # KRfaH
        node_colors[178] = '#A1AF28' # ENusG
        node_colors[124] = '#3CA1AF' # RfaH (original)
        node_colors[84] = '#A62B2E' # 221
        node_colors[62] = '#03FCE8' #212
        node_colors[131] = '#9803FC' #551
        node_colors[28] = '#FC03D7' #541
        node_colors[51] = '#040E6F' #591
        node_alphas = [0.3 for i in range(len(mat))]
        node_alphas[76] = 1.0 # KNusG
        node_alphas[79] = 1.0 # TRfaH
        node_alphas[243] = 1.0 # KRfaH
        node_alphas[178] = 1.0 # ENusG
        node_alphas[124] = 1.0 # RfaH (original)
        node_alphas[84] = 1.0 # 221
        node_alphas[62] = 1.0 #212
        node_alphas[131] = 1.0 #551
        node_alphas[28] = 1.0 #541
        node_alphas[51] = 1.0 #591
        return (node_colors, node_alphas)

def make_colormap():

    teal = [0.0/255, 170.0/255, 170.0/255, 1]
    gray = [170.0/255, 170.0/255, 170.0/255, 1]
    green =[170.0/255, 170.0/255, 0.0/255, 1]
    rose = [199.0/255, 75.0/255, 64.0/255,1]

    x1 = np.linspace(0.0/255, 170.0/255, 1000)
    x2 = np.linspace(170.0/255, 0.0/255, 1000)
    x3 = np.linspace(170.0/255, 170.0/255, 1000)

    #x4 = np.linspace(


    R = np.concatenate([x3, x1])
    G = np.concatenate([x3, x3])
    B = np.concatenate([x2, x3])
    L = np.ones(2000)

    cm = []

    for i in xrange(2000):
            cm.append([R[i],G[i],B[i],L[i]])

    newcmp = ListedColormap(cm)

    return newcmp
    

def get_initial_colors(node_colors):

        node_colorsf = []
        edgecolors = []

        special_cmap = make_colormap()

        for i in xrange(len(node_colors)):

                #print i, node_colors[i]

                if node_colors[i] == -999:
                        print i, node_colors[i]

                #node_colorsf.append(special_cmap(int(node_colors[i]*2000)))
                if node_colors[i] == -999:
                        node_colorsf.append('#777777')
                        edgecolors.append('#777777')
                elif node_colors[i] < 0.5:
                        #node_colorsf.append('#AAAA00')
                        node_colorsf.append('#C74B40')
                        edgecolors.append('#C74B40')
                else:
                        node_colorsf.append('#00AAAA')
                        edgecolors.append('#00AAAA')

        
        node_alphas = [0.5 for i in range(len(node_colors))]
        #Label edges of clusters with experimentally tested variants
        for i in [76,79,243,178,124,62,131,28,51,83]:
                edgecolors[i] = '#000000'
        #node_alphas[76] = 1.0 # KNusG
        #node_alphas[79] = 1.0 # TRfaH
        #node_alphas[243] = 1.0 # KRfaH
        #node_alphas[178] = 1.0 # ENusG
        #node_alphas[124] = 1.0 # RfaH (original)
        #node_alphas[84] = 1.0 # 221
        #node_alphas[62] = 1.0 #212
        #node_alphas[131] = 1.0 #551
        #node_alphas[28] = 1.0 #541
        #node_alphas[51] = 1.0 #591
        #node_alphas[83] = 1.0 #581

        #Change the colors of variants 1 and 7 to represent prediction
        #of specific sequence, not overall node
        node_colorsf[51] = '#00AAAA'
        node_colorsf[83] = '#C74B40'

        return (node_colorsf, node_alphas,edgecolors)
        
# executions sequence
if __name__ == '__main__':
        mat = np.loadtxt(file_mat)
        cluster_d = pd.read_csv(file_cluster, index_col=0) 
        graph = nx.convert_matrix.from_numpy_matrix(mat)
        #node_props = highlight_nodes()

        ncs = open(node_color_scale.pkl)

        node_colors = pickle.load(ncs)

        node_props = get_initial_colors(node_colors)
        
        #print('loading initial coordinates')
        pos = to_dict(read_positions('analysis-22-k30-iter/coord-29.txt'))
        #pos = nx.spring_layout(graph, iterations=iters, k=0.30)

        
        plot_positions(pos, cluster_d, graph, node_colors=node_props[0], \
                       node_alphas=node_props[1],scale=150,edge_colors=node_props[2])
        #plot_labels(pos, graph)
        cbar = plot_edges(pos, graph)
        save_plot('plot_k24_newcolors_updated_120221.png')
