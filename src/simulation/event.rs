use crate::train_lines::{StationId, Time, TrainId};
use std::cmp::Ordering;

#[derive(Debug, Eq, PartialEq)]
pub enum EventKind {
    Start,
    End,
    TrainArrive(TrainId),
    TrainDepart(TrainId),
    PersonArrive(StationId),
}

#[derive(Debug, Eq, PartialEq)]
pub struct Event {
    pub time: Time,
    pub kind: EventKind,
}

impl PartialOrd for Event {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Event {
    fn cmp(&self, other: &Self) -> Ordering {
        // Inverted for inverse ordering
        other.time.cmp(&self.time)
    }
}
