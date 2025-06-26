use crate::train_lines::{StationId, Time};
use petgraph::graphmap::DiGraphMap;
use std::collections::HashMap;
use std::fmt;
use std::fmt::Debug;

pub mod edge;
pub mod node;

use edge::Edge;
use node::Station;

pub struct Graph {
    graph: DiGraphMap<StationId, Edge>,
    stations: HashMap<StationId, Station>,
}

impl Graph {
    pub fn new() -> Self {
        Self {
            graph: DiGraphMap::new(),
            stations: HashMap::new(),
        }
    }

    pub fn get_node(&self, station_id: StationId) -> Option<&Station> {
        self.stations.get(&station_id)
    }

    pub fn get_node_mut(&mut self, station_id: StationId) -> Option<&mut Station> {
        self.stations.get_mut(&station_id)
    }

    pub fn get_edge_mut(&mut self, from: StationId, to: StationId) -> Option<&mut Edge> {
        self.graph.edge_weight_mut(from, to)
    }

    pub fn get_edge(&self, from: StationId, to: StationId) -> Option<&Edge> {
        self.graph.edge_weight(from, to)
    }

    pub fn add_node(&mut self, id: StationId, node: Station) {
        self.stations.insert(id, node);
        self.graph.add_node(id);
    }

    pub fn add_edge(&mut self, from: StationId, to: StationId, distance: Time) {
        self.graph.add_edge(from, to, Edge::new(distance));
    }

    pub fn get_nodes_len(&self) -> usize {
        self.stations.len()
    }
}

impl Debug for Graph {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "GRAPH:\n{:?}", self.graph)?;
        writeln!(f, "\nSTATIONS:")?;
        for (s_id, s) in &self.stations {
            writeln!(f, "{s_id}: {s:?}")?;
        }
        Ok(())
    }
}
