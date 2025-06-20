use crate::train_lines::{Edge, Station, StationId, Train, TrainId, TrainLine};
use itertools::Itertools;
use petgraph::graphmap::DiGraphMap;
use std::collections::HashMap;
use std::rc::Rc;

pub struct TrainSystem {
    pub graph: DiGraphMap<StationId, Edge>,
    pub lines: Vec<Rc<TrainLine>>,
    pub stations: HashMap<StationId, Station>,
    pub trains: HashMap<TrainId, Train>,
    next_train_id: TrainId,
}

impl TrainSystem {
    pub fn new() -> Self {
        Self {
            graph: DiGraphMap::new(),
            lines: vec![],
            stations: HashMap::new(),
            trains: HashMap::new(),
            next_train_id: 0,
        }
    }

    pub fn add_line(&mut self, line: TrainLine) -> Rc<TrainLine> {
        // TODO remove and use map instead
        for (a, b) in line.iter().tuples() {
            self.graph.add_edge(*a, *b, Edge::new());
            self.graph.add_edge(*a, *b, Edge::new());
            self.stations.insert(*a, Station::default());
            self.stations.insert(*b, Station::default());
        }

        let line = Rc::new(line);
        self.lines.push(Rc::clone(&line));

        line
    }

    pub fn add_train(
        &mut self,
        capacity: usize,
        start_station: StationId,
        line: &Rc<TrainLine>,
    ) -> Result<TrainId, ()> {
        let station = self.stations.get_mut(&start_station).ok_or(())?;

        let _ = self
            .trains
            .insert(self.next_train_id, Train::new(Rc::clone(line), capacity));
        station.train_enter();
        self.next_train_id += 1;

        Ok(self.next_train_id - 1)
    }
}
