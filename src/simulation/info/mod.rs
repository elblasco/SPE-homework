use crate::simulation::event::SnapshotKind;
use crate::train_lines::{Direction, Time, TrainId};
use std::fmt;

#[derive(Debug)]
pub struct Info {
    pub time: Time,
    pub kind: InfoKind,
}

#[derive(Debug)]
pub enum InfoKind {
    SimulationStarted(),
    SimulationEnded(),
    PersonArrived {
        station_name: String,
        line_name: String,
        direction: Direction,
    },
    TimedSnapshot(SnapshotKind),
    TrainDeparture {
        train_id: TrainId,
        line_name: String,
        departing_station_name: String,
        // total at the end of loading
        total_passengers: usize,
        loaded_passengers: usize,
        train_capacity: usize,
    },
    TrainArrival {
        train_id: TrainId,
        line_name: String,
        arriving_station_name: String,
        // total at the end of unloading
        total_passengers: usize,
        unloaded_passengers: usize,
        train_capacity: usize,
    },
    TrainCrashed {
        train_id: TrainId,
        line_name: String,
        from_station: String,
        to_station: String,
    },
    TrainRecovered {
        train_id: TrainId,
        line_name: String,
        from_station: String,
        to_station: String,
    },
    WaitingForEdge {
        train_id: TrainId,
        start_station_name: String,
        end_station_name: String,
    },
    FinishedWarmup,
}

impl fmt::Display for Info {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[{}] {}", self.time, self.kind)
    }
}

impl fmt::Display for InfoKind {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::SimulationStarted() => write!(f, "Simulation started"),
            Self::SimulationEnded() => write!(f, "Simulation ended"),
            Self::PersonArrived {
                station_name,
                line_name,
                direction,
            } => write!(
                f,
                "Person arrived at station '{station_name}' on line '{line_name}' heading {direction:?}"
            ),
            Self::TrainDeparture {
                train_id,
                line_name,
                departing_station_name,
                total_passengers,
                loaded_passengers,
                train_capacity,
            } => write!(
                f,
                "Train {train_id:?} line '{line_name}' [{total_passengers} (+{loaded_passengers}) / {train_capacity}] depart '{departing_station_name}'"
            ),
            Self::TrainArrival {
                train_id,
                line_name,
                arriving_station_name,
                total_passengers,
                unloaded_passengers,
                train_capacity,
            } => write!(
                f,
                "Train {train_id:?} line '{line_name}' [{total_passengers} (-{unloaded_passengers}) / {train_capacity}] arrive '{arriving_station_name}'"
            ),
            Self::WaitingForEdge {
                train_id,
                start_station_name,
                end_station_name,
            } => write!(
                f, // TODO add line name
                "Train {train_id:?} waiting on free space on edge from '{start_station_name}' to '{end_station_name}'"
            ),
            Self::TimedSnapshot(kind) => write!(f, "Timed Snapshot: {kind:?}"),
            Self::TrainCrashed {
                train_id,
                line_name,
                from_station,
                to_station,
            } => write!(
                f,
                "Train {train_id:?} crashed when in line {line_name} from '{from_station}' to '{to_station}'"
            ),
            Self::TrainRecovered {
                train_id,
                line_name,
                from_station,
                to_station,
            } => write!(
                f,
                "Train {train_id:?} recovered when in line {line_name} from '{from_station}' to '{to_station}'"
            ),
            Self::FinishedWarmup => write!(f, "Finished warmup"),
        }
    }
}
