import os
# import shapely.errors
# from bs4 import BeautifulSoup
# from plan import Plan
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import json

def visualize(G):
    pos = nx.spring_layout(G)
    weights = nx.get_edge_attributes(G,"weight")
    nx.draw_networkx_nodes(G,pos,node_size=500)
    nx.draw_networkx_edges(G,pos,style = 'solid')
    nx.draw_networkx_labels(G,pos,font_size=10)
    nx.draw_networkx_edge_labels(G, pos,edge_labels= weights,font_color='y')
#%%
def merge(G, n1, n2):
    if(G.has_node(n1)):
        for i in nx.neighbors(G,n1):
            if(i != n2):
                G.add_edge(i,n2)
    else:
        return
    G.remove_node(n1)

def dict_to_graph(dict):
    G = nx.Graph()
    for room in dict.keys():
        adj_rooms = dict[room]
        for adj_room in adj_rooms.keys():
            G.add_edge(room,adj_room,weight = adj_rooms[adj_room])
    return G

def svg_to_json(input_file_path,output_file_path,i):
    input_path = os.path.join(input_file_path,"{}".format(i), 'model.svg')
    if os.path.isfile(input_path):
        with open(input_path) as f:
            content = f.read()
        try:
            soup = BeautifulSoup(content, 'lxml')
            # Create a Plan instance using SVG
            plan = Plan(soup.find('svg'))
            # Calculate room relation
            plan.generate_room_relation()
        except shapely.errors.TopologicalError as e:
            print(e)
        # See graph as adjacency list
        # 0 - Not-connect, 1 - Adjacent, 2 - Door-connect
        dict = plan.get_adjacency_list()

        output_path = os.path.join(output_file_path, "{}.json".format(i))
        if(os.path.isfile(output_path)):
            os.remove(output_path)

        with open(output_path, 'w') as file:
            json.dump(dict,file)


def svg_to_G(input_file_path,i):
    input_path = os.path.join(input_file_path,"{}".format(i), 'model.svg')
    if os.path.isfile(input_path):
        with open(input_path) as f:
            content = f.read()
        try:
            soup = BeautifulSoup(content, 'lxml')
            # Create a Plan instance using SVG
            plan = Plan(soup.find('svg'))

            # Calculate room relation
            plan.generate_room_relation()
        except shapely.errors.TopologicalError as e:
            print(e)
        dict = plan.get_adjacency_list()
        return dict_to_graph(dict)

def remove(G,n):
    for i in range(1,10):
        node = n +'_{}'.format(i)
        if G.has_node(node):
            list = []
            for neighbor in nx.neighbors(G,node):
                list.append(neighbor)
            for i in range(len(list)):
                for j in range(i+1,len(list)):
                    G.add_edge(list[i],list[j])
            G.remove_node(node)
        else:
            return

def merge(G,n1,n2):
    if G.has_node(n1) and G.has_node(n2):
        node_set = set()
        for neighbor_1 in nx.neighbors(G,n1):
            node_set.add(neighbor_1)
        for neighbor_2 in nx.neighbors(G,n2):
            node_set.add(neighbor_2)
        node_set.remove(n1)
        node_set.remove(n2)
        G.remove_node(n1)
        G.remove_node(n2)
        for i in node_set:
            G.add_edge(n1,i)
    else:
        return
def cal_num(G,name):
    num = 0
    for node in G.nodes:
        if (G.nodes[node]['class'] == name):
            num += 1
    return num

def relabel(G):
    mapping ={}
    for node in G.nodes:
        re_node = node.rstrip("_0123456789")
        re_node = re_node.replace('_','')
        mapping[node] = re_node
    re_G = nx.relabel_nodes(G,mapping,copy=False)
    return re_G

delete_room = {'Room',
               'Wardrobe',
               'Entryway',
               'Hall',
               'Balcony',
               'Gym',
               'Unknown',
               'Bathroom',
               'Storage',
               'Garage',
               'GuestRoom',
               'Hallway',
               'Lobby',
               'DiningRoom',
               'Office',
               'LivingRoom',
               'Toilet',
               'Boilerroom',
               'Kitchen',
               'Terrace',
               'Loggia',
               'Aeration',
               'Passengerelevator',
               'Freightelevator',
               'ChildRoom',
               'Bedroom'}
def delete_choice(G):
    for i in delete_room:
        return G.has_node(i)