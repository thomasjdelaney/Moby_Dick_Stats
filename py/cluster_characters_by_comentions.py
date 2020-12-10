"""
For calculating the normalised character comentions matrix and applying the
Spectral rejection algorithm to the matrix, to cluster the characters.
"""
import os, sys, argparse, re, nltk, shutil
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from moby_dick_functions import *

np.set_printoptions(linewidth=shutil.get_terminal_size().columns)

proj_dir = os.path.join(os.environ.get('HOME'), 'Moby_Dick_Stats')
txt_dir = os.path.join(proj_dir, 'txt')
image_dir = os.path.join(proj_dir, 'images')
moby_dick_txt_file = os.path.join(txt_dir, 'moby_dick.txt')
character_list_file = os.path.join(txt_dir, 'character_list.txt')

sys.path.append(os.environ['PROJ'])
import Network_Noise_Rejection_Python as nnr

def plotCharacterComentionsSave(total_mentions, normed_chapter_mentions, character_list):
    """
    For sorting and plotting the character co-mentions.
    Arguments:  total_mentions, the total number of chapters in which each character is mentioned
                normed_chapter_mentions, matrix of character co-mentions
                character_list, list of str
    Returns:    file_name where the figure is saved.
    """
    sorted_inds = np.argsort(total_mentions)
    sorted_normed_chapter_mentions = normed_chapter_mentions[:,sorted_inds[::-1]]; sorted_normed_chapter_mentions = sorted_normed_chapter_mentions[sorted_inds[::-1],:]
    sorted_character_list = np.array(character_list)[sorted_inds[::-1]]
    plotChapterCoMentions(sorted_normed_chapter_mentions, sorted_character_list, title='Normed chracter co-mentions', figsize=(10,8))
    save_name = os.path.join(image_dir, 'normed_character_comentions_full_novel.png')
    plt.savefig(save_name)
    return save_name

def getLeavesKeeps(graph_network_matrix):
    """
    Get the leaf nodes, nodes to keep, and the degree distribution of the network represented by the given graph network matrix.
    Arguments:  graph_network_matrix, numpy array (square matrix)
    Returns:    degree_distn, the degree of each node
                leaf_inds, the indices of the leaf nodes
                keep_inds, the indices of the nodes to keep.
    """
    degree_distn = (graph_network_matrix > 0).sum(axis=0)
    leaf_inds = np.flatnonzero(degree_distn == 1)
    keep_inds = np.flatnonzero(degree_distn > 1)
    return degree_distn, leaf_inds, keep_inds

with open(moby_dick_txt_file, 'r') as f:
    moby_dick_text = f.read()

num_to_chap_title = extractChapterTitleDict(moby_dick_text)
character_list_with_doubles = getCharacterList(character_list_file)
character_count_dict = getCharacterCounts(moby_dick_text, character_list_with_doubles)
character_list = list(character_count_dict.keys())
normed_chapter_mentions, total_mentions = getNormedCharacterCoMentions(character_list, num_to_chap_title, moby_dick_text, character_list_with_doubles)
normed_chapter_mentions = nnr.checkDirected(normed_chapter_mentions.copy())
normed_chapter_mentions_comp, keep_indices, comp_assign, comp_size = nnr.getBiggestComponent(normed_chapter_mentions.copy())
null_samples_eig_vals, optional_returns = nnr.getPoissonWeightedConfModel(normed_chapter_mentions_comp, 100, return_eig_vecs=True, is_sparse=True)
null_samples_eig_vecs = optional_returns['eig_vecs']
expected_sparse_wcm = optional_returns['expected_wcm']
print(dt.datetime.now().isoformat() + ' INFO: ' + 'Constructing network modularity matrix...')
network_modularity_matrix = normed_chapter_mentions_comp - expected_sparse_wcm
print(dt.datetime.now().isoformat() + ' INFO: ' + 'Getting low dimensional space...')
below_eig_space, below_lower_bound_inds, [mean_mins_eig, min_confidence_ints], exceeding_eig_space, exceeding_upper_bound_inds, [mean_maxs_eig, max_confidence_ints] = nnr.getLowDimSpace(network_modularity_matrix, null_samples_eig_vals, 0, int_type='CI')
exceeding_space_dims = exceeding_eig_space.shape[1]
below_space_dims = below_eig_space.shape[1]
reject_dict = nnr.nodeRejection(network_modularity_matrix, null_samples_eig_vals, 0, null_samples_eig_vecs, weight_type='linear', norm='L2', int_type='CI', bounds='upper')
signal_normed_chapter_mentions = normed_chapter_mentions_comp[reject_dict['signal_inds']][:, reject_dict['signal_inds']]
if reject_dict['signal_inds'].size == 0:
    print(dt.datetime.now().isoformat() + ' WARN: ' + 'No signal network!')
    noise_final_cell_info = cell_info.loc[cell_ids[reject_dict['noise_inds']]]
else:
    print(dt.datetime.now().isoformat() + ' INFO: ' + 'Constructing final signal network without leaves...')
    biggest_signal_normed_chapter_mentions_comp, biggest_signal_normed_chapter_mentions_comp_inds, biggest_signal_normed_chapter_mentions_comp_assign, biggest_signal_normed_chapter_mentions_comp_size = nnr.getBiggestComponent(signal_normed_chapter_mentions)
    biggest_signal_normed_chapter_mentions_comp_inds = reject_dict['signal_inds'][biggest_signal_normed_chapter_mentions_comp_inds]
    degree_distn, leaf_inds, keep_inds = getLeavesKeeps(biggest_signal_normed_chapter_mentions_comp)
    final_normed_chapter_mentions_inds = biggest_signal_normed_chapter_mentions_comp_inds[keep_inds]
    signal_normed_chapter_mentions_leaf_inds = biggest_signal_normed_chapter_mentions_comp_inds[leaf_inds]
    final_normed_chapter_mentions = biggest_signal_normed_chapter_mentions_comp[keep_inds][:, keep_inds]
    final_character_list = np.array(character_list)[final_normed_chapter_mentions_inds]
    leaf_characters = np.array(character_list)[signal_normed_chapter_mentions_leaf_inds]
    noise_characters = np.array(character_list)[reject_dict['noise_inds']]
    print(dt.datetime.now().isoformat() + ' INFO: ' + 'Leaf characters are: ' + ', '.join(leaf_characters)) if len(leaf_characters) > 0 else None
    print(dt.datetime.now().isoformat() + ' INFO: ' + 'Noise characters are: ' + ', '.join(noise_characters)) if len(noise_characters) > 0 else None

    print(dt.datetime.now().isoformat() + ' INFO: ' + 'Detecting communities...')
    signal_expected_wcm = expected_sparse_wcm[final_normed_chapter_mentions_inds][:, final_normed_chapter_mentions_inds]
    max_mod_cluster, max_modularity, consensus_clustering, consensus_modularity, consensus_iterations, is_converged = nnr.consensusCommunityDetect(final_normed_chapter_mentions, signal_expected_wcm, exceeding_space_dims+1, exceeding_space_dims+1)

# saved_name = plotCharacterComentionsSave(total_mentions, normed_chapter_mentions, character_list)
# print(dt.datetime.now().isoformat() + ' INFO: ' + saved_name + ' saved.')
