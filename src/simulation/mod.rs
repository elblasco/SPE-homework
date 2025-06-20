#![allow(dead_code)]
mod event;
mod simulate;
mod train_system;

use crate::simulation::event::{Event, EventKind};
use crate::train_lines::Time;
use std::collections::BinaryHeap;
pub use train_system::TrainSystem;

pub struct Simulation {
    events: BinaryHeap<Event>,
    sys: TrainSystem,
    // TODO add parameters to record, then print in csv
}

impl Simulation {
    fn new(start_time: Time, end_time: Time) -> Self {
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
            events,
            sys: TrainSystem::new(),
        }
    }
}
