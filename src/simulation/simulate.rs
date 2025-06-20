use crate::simulation::{Event, EventKind, Simulation};
use crate::train_lines::{Time, TrainId};

impl Simulation {
    pub fn simulation_step(&mut self) -> Result<bool, ()> {
        let Event { time, kind } = self.events.pop().unwrap();

        match kind {
            EventKind::Start => {}
            EventKind::End => return Ok(true),
            EventKind::TrainArrive(train_id) => {
                let new_event = self.train_arrive(time, train_id).ok_or(())?;
                self.events.push(new_event);
            } // TODO FIx
            EventKind::TrainDepart(train_id) => {
                let new_event = self.train_depart(time, train_id).ok_or(())?;
                self.events.push(new_event);
            } // TODO fix
            EventKind::PersonArrive(_station) => todo!(),
        }

        Ok(false)
    }

    fn train_arrive(&mut self, time: Time, train_id: TrainId) -> Option<Event> {
        let train = self.sys.trains.get_mut(&train_id)?;

        let exited_station_id = train.get_curr_station();
        let (entering_station_id, _) = train.get_next_station();

        let curr_station = self.sys.stations.get_mut(&entering_station_id)?;
        curr_station.train_enter();

        train.go_next_stop();

        let edge = self
            .sys
            .graph
            .edge_weight_mut(exited_station_id, entering_station_id)?;
        edge.train_exit().unwrap(); // TODO SHOULD ABSOLUTELY NOT BE AN UNWRAP
        let arrival_time = time
            + if exited_station_id == entering_station_id {
                1
            } else {
                edge.get_distance()
            };
        Some(Event {
            time: arrival_time,
            kind: EventKind::TrainDepart(train_id),
        })
    }

    fn train_depart(&mut self, time: Time, train_id: TrainId) -> Option<Event> {
        let train = self.sys.trains.get(&train_id)?;

        let start = train.get_curr_station();
        let (end, _) = train.get_next_station();

        // TODO not use 1
        let arrival_time = time
            + if start == end {
                1
            } else {
                self.sys.graph.edge_weight(start, end)?.get_distance()
            };

        let curr_station = self.sys.stations.get_mut(&start)?;
        curr_station.train_exit();

        let edge = self.sys.graph.edge_weight_mut(start, end)?;
        edge.train_enter().unwrap(); // TODO SHOULD ABSOLUTELY NOT BE AN UNWRAP

        Some(Event {
            time: arrival_time,
            kind: EventKind::TrainArrive(train_id),
        })
    }
}
