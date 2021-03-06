import numpy as np
import os
from sklearn.decomposition import TruncatedSVD


def get_weighted_average(We, x, w):
    """
    Compute the weighted average vectors
    :param We: We[i,:] is the vector for word i
    :param x: x[i, :] are the indices of the words in sentence i
    :param w: w[i, :] are the weights for the words in sentence i
    :return: emb[i, :] are the weighted average vector for sentence i
    """
    We = np.array(We)
    print('size of We', We.shape)
    print('size of x', x.shape)
    n_samples = x.shape[0]
    # n_samples = x.shape[1]
    print("the number of samples is {}".format(n_samples))
    emb = np.zeros((n_samples, We.shape[1]))
    print("shape of emb {}".format(emb.shape))
    for i in xrange(n_samples):
        emb[i,:] = w[i,:].dot(We[x[i,:],:]) / np.count_nonzero(w[i,:])
    return emb

def compute_pc(X, npc):
    """
    Compute the principal components. DO NOT MAKE THE DATA ZERO MEAN!
    :param X: X[i,:] is a data point
    :param npc: number of principal components to remove
    :return: component_[i,:] is the i-th pc
    """
    svd = TruncatedSVD(n_components=npc, n_iter=7, random_state=0)
    svd.fit(X)
    return svd.components_

def remove_pc(X, npc, fpc_file):
    """
    Remove the projection on the principal components
    :param X: X[i,:] is a data point
    :param npc: number of principal components to remove
    :return: XX[i, :] is the data point after removing its projection
    """
    pc = 0.8 * load_pc(fpc_file)
    print("shape of pc:", np.shape(pc))
    if npc==1:
        XX = X - X.dot(pc.transpose()) * pc
    else:
        XX = X - X.dot(pc.transpose()).dot(pc)
    return XX

def load_pc(filename):
    path2file = os.path.join("../first_principal_component/", filename)
    return np.load(path2file)

def SIF_embedding(We, x, w, params, fpc_file):
    """
    Compute the scores between pairs of sentences using weighted average + removing the projection on the first principal component
    :param We: We[i,:] is the vector for word i
    :param x: x[i, :] are the indices of the words in the i-th sentence
    :param w: w[i, :] are the weights for the words in the i-th sentence
    :param params.rmpc: if >0, remove the projections of the sentence embeddings to their first principal component
    :return: emb, emb[i, :] is the embedding for sentence i
    """
    emb = get_weighted_average(We, x, w)
    print("shape of emb:", np.shape(emb))
    if params.rmpc > 0:
        emb = remove_pc(emb, params.rmpc, fpc_file)
    return emb


def calculate_first_pc(We, x, w, params, fpc_file):
    emb = get_weighted_average(We, x, w)
    if params.rmpc > 0:
        pc = compute_pc(emb, params.rmpc)
        save_1pc(pc, fpc_file)

def save_1pc(pc, fpc_file):
    fpc_file += '_lawinsider_full'
    path2file = os.path.join("../first_principal_component/", fpc_file)
    np.save(open(path2file, 'wb'), pc)
    print("The 1pc file generated by {} has been saved.".format(fpc_file))


"""
    this part is made for experiment of second principal component.
"""
# def calculate_second_pc(We, x, w, params, fpc_file):
#     emb = get_weighted_average(We, x, w)
#     if params.rmpc > 0:
#         pc = compute_pc(emb, params.rmpc)
#         secondPC = pc[1].reshape((1, 300))
#         save_2pc(secondPC, fpc_file)
#
# def save_2pc(pc, fpc_file):
#     fpc_file += '_2pc'
#     path2file = os.path.join("../second_principal_component/", fpc_file)
#     np.save(open(path2file, 'wb'), pc)
#     print("The 2pc file generated by {} has been saved.".format(fpc_file))
#
# def remove_2pc(X, npc, fpc_file):
#     """
#     Remove the projection on the principal components
#     :param X: X[i,:] is a data point
#     :param npc: number of principal components to remove
#     :return: XX[i, :] is the data point after removing its projection
#     """
#     second_pc = load_2pc(fpc_file)
#     XX = X - X.dot(second_pc.transpose()) * second_pc
#     return XX
#
# def load_2pc(filename):
#     path2file = os.path.join("../second_principal_component/", filename)
#     return np.load(path2file)