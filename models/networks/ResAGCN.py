from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals


import tensorflow as tf

from AGCN.models.networks.basic_networks import SimpleAGCN
from AGCN.models.tf_modules.tf_graphs import ResidualGraphMol
from AGCN.models.layers import DenseMol, SGC_LL, GraphGatherMol, GraphPoolMol, BlockEnd
from AGCN.models.tf_modules.multitask_classifier import MultitaskGraphClassifier


class ResAGCN(SimpleAGCN):
    def construct_network(self):
        tf.set_random_seed(self.seed)

        n_features = self.data['train'].get_raw_feature_n()
        batch_size = self.hyper_parameters['batch_size']
        K = self.hyper_parameters['max_hop_K']
        n_filters = self.hyper_parameters['n_filters']  # SGL_LL output dimensions
        final_feature_n = self.hyper_parameters['final_feature_n']
        learning_rate = self.hyper_parameters['learning_rate']
        beta1 = self.hyper_parameters['optimizer_beta1']
        beta2 = self.hyper_parameters['optimizer_beta2']
        optimizer_type = self.hyper_parameters['optimizer_type']

        """ Residual Network Architecture - 3 residual blocks 6 SGC layers"""
        self.graph_model = ResidualGraphMol(n_features, batch_size, self.max_atom)
        """ block start """
        self.graph_model.add(SGC_LL(n_filters, n_features, batch_size, K=K, activation='relu'))
        self.graph_model.add(SGC_LL(n_filters, n_filters, batch_size, K=K, activation='relu'))
        self.graph_model.add(BlockEnd(self.max_atom, batch_size))
        """ block end """
        self.graph_model.add(SGC_LL(n_filters, n_filters, batch_size, K=K, activation='relu'))
        self.graph_model.add(SGC_LL(n_filters, n_filters, batch_size, K=K, activation='relu'))
        self.graph_model.add(BlockEnd(self.max_atom, batch_size))

        self.graph_model.add(SGC_LL(n_filters, n_filters, batch_size, K=K, activation='relu'))
        self.graph_model.add(SGC_LL(n_filters, n_filters, batch_size, K=K, activation='relu'))
        self.graph_model.add(BlockEnd(self.max_atom, batch_size))

        self.graph_model.add(DenseMol(final_feature_n, n_filters, activation='relu'))
        self.graph_model.add(GraphGatherMol(batch_size, activation="tanh"))

        """ Classifier """
        self.classifier = MultitaskGraphClassifier(
            self.graph_model,
            len(self.tasks),
            batch_size=batch_size,
            learning_rate=learning_rate,
            optimizer_type=optimizer_type,
            beta1=beta1,
            beta2=beta2,
            n_feature=final_feature_n
        )
        print("Network Constructed Successfully! \n")


class LongResAGCN(ResAGCN):
    def construct_network(self):
        tf.set_random_seed(self.seed)

        n_features = self.data['train'].get_raw_feature_n()
        batch_size = self.hyper_parameters['batch_size']
        K = self.hyper_parameters['max_hop_K']
        n_filters = self.hyper_parameters['n_filters']  # SGL_LL output dimensions
        final_feature_n = self.hyper_parameters['final_feature_n']
        learning_rate = self.hyper_parameters['learning_rate']
        beta1 = self.hyper_parameters['optimizer_beta1']
        beta2 = self.hyper_parameters['optimizer_beta2']
        optimizer_type = self.hyper_parameters['optimizer_type']

        """ Residual Network Architecture - 6 residual blocks 12 SGC layers"""
        self.graph_model = ResidualGraphMol(n_features, batch_size, self.max_atom)

        self.graph_model.add(SGC_LL(n_filters, n_features, batch_size, K=K, activation='relu'))
        self.graph_model.add(SGC_LL(n_filters, n_filters, batch_size, K=K, activation='relu'))
        self.graph_model.add(BlockEnd(self.max_atom, batch_size))

        self.graph_model.add(SGC_LL(n_filters, n_filters, batch_size, K=K, activation='relu'))
        self.graph_model.add(SGC_LL(n_filters, n_filters, batch_size, K=K, activation='relu'))
        self.graph_model.add(BlockEnd(self.max_atom, batch_size))

        self.graph_model.add(SGC_LL(n_filters, n_filters, batch_size, K=K, activation='relu'))
        self.graph_model.add(SGC_LL(n_filters, n_filters, batch_size, K=K, activation='relu'))
        self.graph_model.add(BlockEnd(self.max_atom, batch_size))

        self.graph_model.add(SGC_LL(n_filters, n_features, batch_size, K=K, activation='relu'))
        self.graph_model.add(SGC_LL(n_filters, n_filters, batch_size, K=K, activation='relu'))
        self.graph_model.add(BlockEnd(self.max_atom, batch_size))

        self.graph_model.add(SGC_LL(n_filters, n_filters, batch_size, K=K, activation='relu'))
        self.graph_model.add(SGC_LL(n_filters, n_filters, batch_size, K=K, activation='relu'))
        self.graph_model.add(BlockEnd(self.max_atom, batch_size))

        self.graph_model.add(SGC_LL(n_filters, n_filters, batch_size, K=K, activation='relu'))
        self.graph_model.add(SGC_LL(n_filters, n_filters, batch_size, K=K, activation='relu'))
        self.graph_model.add(BlockEnd(self.max_atom, batch_size))

        self.graph_model.add(DenseMol(final_feature_n, n_filters, activation='relu'))
        self.graph_model.add(GraphGatherMol(batch_size, activation="tanh"))

        """ Classifier """
        self.classifier = MultitaskGraphClassifier(
            self.graph_model,
            len(self.tasks),
            batch_size=batch_size,
            learning_rate=learning_rate,
            optimizer_type=optimizer_type,
            beta1=beta1,
            beta2=beta2,
            n_feature=final_feature_n
        )
        print("Network Constructed Successfully! \n")