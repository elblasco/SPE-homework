use crate::train_lines::{StationId, Time, TrainId};
use std::cmp::Ordering;

#[derive(Debug, Eq, PartialEq, Clone)]
pub enum SnapshotKind {
    PeopleInStation,
}

#[derive(Debug, Eq, PartialEq, Clone)]
pub enum EventKind {
    Start,
    End,
    TimedSnapshot(SnapshotKind),
    TrainArrive(TrainId),
    TrainDepart(TrainId),
    PersonArrive(StationId),
}

#[derive(Debug, Clone)]
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
        f64::total_cmp(&other.time, &self.time)
    }
}

impl PartialEq for Event {
    fn eq(&self, other: &Self) -> bool {
        other.time == self.time
    }
}

impl Eq for Event {}
