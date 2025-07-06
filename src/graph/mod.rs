use crate::train_lines::StationId;
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

    pub fn get_node(&self, station_id: StationId) -> Result<&Station, String> {
        self.stations
            .get(&station_id)
            .ok_or_else(|| "Station does not exist".to_string())
    }

    pub fn get_node_mut(&mut self, station_id: StationId) -> Result<&mut Station, String> {
        self.stations
            .get_mut(&station_id)
            .ok_or_else(|| "Station does not exist".to_string())
    }

    pub fn get_edge_mut(&mut self, from: StationId, to: StationId) -> Result<&mut Edge, String> {
        self.graph
            .edge_weight_mut(from, to)
            .ok_or_else(|| "Edge does not exist".to_string())
    }

    pub fn get_edge(&self, from: StationId, to: StationId) -> Result<&Edge, String> {
        self.graph
            .edge_weight(from, to)
            .ok_or_else(|| "Edge does not exist".to_string())
    }

    pub fn add_node(&mut self, id: StationId, node: Station) {
        self.stations.insert(id, node);
        self.graph.add_node(id);
    }

    pub fn add_edge(&mut self, from: StationId, to: StationId, distance: f64, max_capacity: usize) {
        self.graph
            .add_edge(from, to, Edge::new(distance, max_capacity));
    }

    pub(crate) fn iter_station_id(&self) -> impl Iterator<Item = &StationId> {
        self.stations.keys()
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
