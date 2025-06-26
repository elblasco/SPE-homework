mod event;
mod info;
mod simulate;
mod train_system;

use crate::dataset::StationData;
use crate::graph::Graph;
use crate::graph::node::Station;
pub use crate::simulation::event::{Event, EventKind};
use crate::train_lines::line::Line;
use crate::train_lines::train::Train;
use crate::train_lines::{StationId, Time, TrainId};
use crate::utils::time::{from_minutes, from_seconds};
pub use info::InfoKind;
use rand_distr::Exp;
use std::collections::{BinaryHeap, HashMap, VecDeque};
use std::fmt;
use std::fmt::Debug;
use std::rc::Rc;

pub struct Simulation {
    graph: Graph,
    lines: Vec<Rc<Line>>,
    trains: HashMap<TrainId, Train>,
    next_train_id: TrainId,
    distr_train_at_station: Exp<Time>,
    events: BinaryHeap<Event>,
    train_waiting: HashMap<(StationId, StationId), VecDeque<TrainId>>,
}

impl Simulation {
    pub fn new(start_time: Time, end_time: Time, stations: &[StationData]) -> Self {
        let mut new = Self {
            graph: Graph::new(),
            lines: vec![],
            trains: HashMap::new(),
            next_train_id: 0,
            events: Self::get_initial_events(start_time, end_time),
            distr_train_at_station: Exp::new(1.0 / from_seconds(20.0)).unwrap(),
            train_waiting: HashMap::new(),
        };

        for (idx, data) in stations.iter().enumerate() {
            new.graph.add_node(
                idx,
                Station::new(&data.name, data.lat, data.lon, from_minutes(1.0)),
            );
        }

        new
    }

    fn get_initial_events(start_time: Time, end_time: Time) -> BinaryHeap<Event> {
        BinaryHeap::from([
            Event {
                time: start_time,
                kind: EventKind::Start,
            },
            Event {
                time: end_time,
                kind: EventKind::End,
            },
        ])
    }

    pub fn iter_trains(&self) -> impl Iterator<Item = &Train> {
        self.trains.values()
    }
}

impl Debug for Simulation {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "SIMULATION")?;
        writeln!(f, "\nMAP:\n{:?}", self.graph)?;
        writeln!(f, "\nLINES:")?;
        for (l_id, l) in self.lines.iter().enumerate() {
            writeln!(f, "{l_id}: {l:?}")?;
        }
        writeln!(f, "\nTRAINS:")?;
        for (t_id, t) in &self.trains {
            writeln!(f, "{t_id}: {t:?}")?;
        }
        writeln!(f, "\nEVENTS: pending events {}", self.events.len(),)?;
        Ok(())
    }
}
