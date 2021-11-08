#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 14:26:23 2021

@author: candysansores
"""

import networkx as nx
from matplotlib import pyplot as plt
import InstanciasdeGrafos as I

class Clique(): #3clique)
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w
        self.leader = None
        
    def get_vertices(self):
        return [u, v, w]

class Node(): #(vértice)
    def __init__(self, id):
        self.id=id
        self.delta=False
        self.clique3=[]
        self.cliques=[]
        self.hub=False    #True si el nodo es parte del hub
        self.neighbors=[] #lista de vértices vecinos
        self.covered=False
        
    #def add_neighbors(self, neighbors):
    #   self.neighbors=neighbors   
        
    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor) 
    
    def add_clique(self, clique):
        self.cliques.append(clique)
    
    def get_id(self):
        return self.id
    
    def get_delta_neighbors(self):
        s=set()
        neigh=[]
        if self.delta:
            for c in self.clique3:
                s.update({i for i in c if i!=self.id})
            for delta_neigh in s:
                for n in self.neighbors:
                    if delta_neigh == n.id:
                        neigh.append(n)
        return neigh
    
    def get_deltas_withoutleader(self):
        deltas=[]
        for d in self.cliques:
            if not d.leader:
                deltas.append(d)
        return deltas     
        
    def get_delta_u_w(self):
        s=set()
        uw=[]
        if self.delta:
            for c in self.clique3:
                s={i for i in c if i!=self.id}
                uw.append(s)
        return uw
    
    def is_leader(self):
        leader=False
        deltas_withoutleader=self.get_deltas_withoutleader() #TSL=triángulos_sin_lider
        mydeltas_withoutleader_cardinality=len(deltas_withoutleader) #cardinalidad de TSL
        for delta_neigh in self.get_delta_neighbors(): #para cada vecino en mis triángulos
            neighbordeltas_withoutleader_cardinality=len(delta_neigh.get_deltas_withoutleader()) #calcula cardinalidad TSL
            if mydeltas_withoutleader_cardinality > neighbordeltas_withoutleader_cardinality:
                leader=True
            else:
                if mydeltas_withoutleader_cardinality == neighbordeltas_withoutleader_cardinality:
                    if self.id>delta_neigh.id:
                        leader=True
                    else:
                        leader=False
                        break
                else:
                    leader=False
                    break
        if leader:
            for delta_neigh in self.get_delta_neighbors():
                for delta in delta_neigh.get_deltas_withoutleader():
                    delta.leader=self.id
                    #for vertice in delta.get_vertices():
                    #    vertice.leader=self.id              
        return leader
        
    def get_grade(self):
        return len(self.neighbors) 
    
    def get_delta_cardinality(self):
        return len(self.clique3)
    
    def __str__(self):
        return f'({self.get_id()}'
    
    
if __name__=='__main__':
    #Create a random graph
    # nodes = 8
    # probability = 0.6
    # seed = 11
    # g = nx.gnp_random_graph(nodes, probability, seed)
    g = I.instancia12()
    graphnodes=[]
    for v in g[0].nodes:
        n=Node(v)
        graphnodes.append(n)
    for v in graphnodes:
        Nv=list(g[0].neighbors(v.id))
        for nid in Nv:
            for n in graphnodes:
                if nid==n.id:
                    v.add_neighbor(n)
                    
    color_lookup = {k:v for v, k in enumerate(sorted(set(g[0].nodes())))}    
    nx.draw(g[0], 
        nodelist=color_lookup,
        node_size=500,
        node_color=[n.is_leader() for n in graphnodes], with_labels=True,
        pos = g[1])
    plt.show() 
    
    for v in graphnodes: #for v in g.nodes:
        for u in v.neighbors:
            for w in v.neighbors:
                clique=set()
                if w.id != u.id:
                    if (u.id,w.id) in g[0].edges:
                        v.delta=True
                        clique.update({u.id, v.id, w.id})
                        cliqueObj=Clique(u,v,w)
                        notequal=True
                        for i in range(len(v.clique3)):
                            if v.clique3[i] == clique:
                                notequal=False
                                break
                        if notequal:
                            v.clique3.append(clique)
                            v.add_clique(cliqueObj)
    for u in graphnodes:
        print("Node: ", u.id)
        #print("Neighbors: ", u.neighbors)
        print("Cliques: ", u.clique3)
        print("UW Pairs: ", u.get_delta_u_w())
        #print("Delta neighbors: ", u.get_delta_neighbors())
        print("Leader: ", u.is_leader())
    
    nx.draw(g[0], 
        nodelist=color_lookup,
        node_size=500,
        node_color=[n.is_leader() for n in graphnodes], with_labels=True,
        pos = g[1])
    plt.show()                  
                