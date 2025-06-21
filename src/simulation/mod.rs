mod event;
mod info;
mod simulate;
mod train_system;

use crate::graph::Graph;
pub use crate::simulation::event::{Event, EventKind};
use crate::simulation::info::Info;
use crate::train_lines::train::Train;
use crate::train_lines::train_line::TrainLine;
use crate::train_lines::{Time, TrainId};
use std::collections::{BinaryHeap, HashMap};
use std::fmt;
use std::fmt::Debug;
use std::rc::Rc;

pub struct Simulation {
    pub graph: Graph,
    pub lines: Vec<Rc<TrainLine>>,
    pub trains: HashMap<TrainId, Train>,
    pub next_train_id: TrainId,

    pub info: Info,
    events: BinaryHeap<Event>,
}

impl Simulation {
    pub fn new(start_time: Time, end_time: Time) -> Self {
        let mut events = BinaryHeap::new();
        events.push(Event {
            time: start_time,
            kind: EventKind::Start,
        });
        events.push(Event {
            time: end_time,
            kind: EventKind::End,
        });

        Self {
            graph: Graph::new(),
            lines: vec![],
            trains: HashMap::new(),
            next_train_id: 0,

            info: Info::default(),
            events,
        }
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
