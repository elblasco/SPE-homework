use crate::train_lines::{Direction, Time, TrainId};

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
    },
    TrainArrival {
        train_id: TrainId,
        line_name: String,
        arriving_station_name: String,
    },
}
