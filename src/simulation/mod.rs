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
use crate::train_lines::{Time, TrainId};
use std::collections::{BinaryHeap, HashMap};
use std::fmt;
use std::fmt::Debug;
use std::rc::Rc;

pub use info::InfoKind;

pub struct Simulation {
    pub graph: Graph,
    pub lines: Vec<Rc<Line>>,
    pub trains: HashMap<TrainId, Train>,
    pub next_train_id: TrainId,

    //pub info: SystemInfo,
    events: BinaryHeap<Event>,
}

impl Simulation {
    pub fn new(start_time: Time, end_time: Time, stations: &[StationData]) -> Self {
        let mut new = Self {
            graph: Graph::new(),
            lines: vec![],
            trains: HashMap::new(),
            next_train_id: 0,
            //info: Info::SimulationStarted(),
            events: Self::get_initial_events(start_time, end_time),
        };

        for (idx, data) in stations.iter().enumerate() {
            new.graph
                .add_node(idx, Station::new(&data.name, data.lat, data.lon));
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

    pub fn peek_event(&self) -> Option<Event> {
        self.events.peek().cloned()
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
