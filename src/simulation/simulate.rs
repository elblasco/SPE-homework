use crate::simulation::{Event, EventKind, Simulation};
use crate::train_lines::train_line::Direction;
use crate::train_lines::{StationId, Time, TrainId};
use rand::Rng;

impl Simulation {
    pub fn simulation_step(&mut self) -> Result<bool, String> {
        let Event { time, kind } = self.events.pop().unwrap();

        match kind {
            EventKind::Start => {
                for (id, _) in &self.trains {
                    self.events.push(Event {
                        time: 0,
                        kind: EventKind::TrainDepart(*id),
                    });
                }

                self.events.push(Event {
                    time: time + 10,
                    kind: EventKind::PersonArrive(rand::rng().random_range(1..5)), // TODO DELETE LINE FIRST APPROACH
                })
            }
            EventKind::End => return Ok(true),
            EventKind::TrainArrive(train_id) => {
                let new_event = self.train_arrive(time, train_id)?;
                self.events.push(new_event);
            } // TODO FIx
            EventKind::TrainDepart(train_id) => {
                let new_event = self.train_depart(time, train_id)?;
                self.events.push(new_event);
            } // TODO fix
            EventKind::PersonArrive(station_id) => {
                let new_event = self.person_arrive(time, station_id)?;
                self.events.push(new_event);
            }
        }

        Ok(false)
    }

    fn person_arrive(&mut self, time: Time, station_id: StationId) -> Result<Event, String> {
        let station = self
            .graph
            .get_node_mut(station_id)
            .ok_or_else(|| "Station does not exist")?;
        let line_stop = station
            .get_random_line_stop_mut()
            .ok_or_else(|| "Station has no line stops")?;
        line_stop.borrow_mut().person_enter(Direction::rand(), 1);

        if self.next_train_id == 0 {
            return Err("No Train".to_string());
        }

        Ok(Event {
            time: time + 10,
            kind: EventKind::PersonArrive(rand::rng().random_range(1..5)),
        })
    }

    fn train_arrive(&mut self, time: Time, train_id: TrainId) -> Result<Event, String> {
        let train = self
            .trains
            .get_mut(&train_id)
            .ok_or_else(|| "Train does not exist")?;

        let exited_station_id = train.get_curr_station();
        let (entering_station_id, _) = train.get_next_station();

        let arrival_time;
        if exited_station_id != entering_station_id {
            let curr_station = self
                .graph
                .get_node_mut(entering_station_id)
                .ok_or_else(|| "Station not found")?;
            curr_station.train_enter();

            let edge = self
                .graph
                .get_edge_mut(exited_station_id, entering_station_id)
                .ok_or_else(|| "Edge not found")?;
            edge.train_exit()
                .map_err(|_| "Cannot remove train because already 0 on edge")?;

            arrival_time = time + edge.get_distance();
        } else {
            arrival_time = time + 1;
        }

        train.go_next_stop();

        Ok(Event {
            time: arrival_time,
            kind: EventKind::TrainDepart(train_id),
        })
    }

    fn train_depart(&mut self, time: Time, train_id: TrainId) -> Result<Event, String> {
        let train = self
            .trains
            .get(&train_id)
            .ok_or_else(|| "Train does not exist")?;

        let start = train.get_curr_station();
        let (end, _) = train.get_next_station();

        let arrival_time;
        if start != end {
            let curr_station = self
                .graph
                .get_node_mut(start)
                .ok_or_else(|| "Current station doesn't exist")?;
            curr_station
                .train_exit()
                .map_err(|_| "Cannot remove train because already 0 on node")?;

            let edge = self
                .graph
                .get_edge_mut(start, end)
                .ok_or_else(|| "Edge doesn't exist")?;
            edge.train_enter();
            arrival_time = time + edge.get_distance();
        } else {
            // TODO not use 1
            arrival_time = time + 1;
        }
        Ok(Event {
            time: arrival_time,
            kind: EventKind::TrainArrive(train_id),
        })
    }
}
