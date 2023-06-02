import numpy as np
import osmnx as ox
import networkx as nx
import geopandas as gpd

from sklearn.neighbors import BallTree

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/range', methods=['GET'])
def cal_range():
    args = request.args
    begin_lat = args.get('begin_lat')
    begin_lng = args.get('begin_lng')
    end_lat = args.get('end_lat')
    end_lng = args.get('end_lng')
    # begin_latlng = (18.807051, 99.023283)
    # end_latlng = (18.800674, 99.023021) 
    begin_latlng = (float(begin_lat),float(begin_lng))
    end_latlng = (float(end_lat),float(end_lng))

    G = ox.graph_from_point(start_latlng, dist=2000, network_type='drive', simplify=False) 
    orig_node = ox.nearest_nodes(G, start_latlng[1], start_latlng[0])
    dest_node = ox.nearest_nodes(G, end_latlng[1], end_latlng[0])
    shortest_route = nx.shortest_path(G, orig_node, dest_node, method='bellman-ford',weight='length')
    lenght = nx.shortest_path_length(G, orig_node, dest_node, weight='length')
    return lenght