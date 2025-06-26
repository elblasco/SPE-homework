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
                "Train {train_id:?} departed from '{departing_station_name}' on line '{line_name}'. Loaded: {loaded_passengers}, Total: {total_passengers}, Capacity: {train_capacity}"
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
                "Train {train_id:?} arrived at '{arriving_station_name}' on line '{line_name}'. Unloaded: {unloaded_passengers}, Total: {total_passengers}, Capacity: {train_capacity}"
            ),
        }
    }
}
