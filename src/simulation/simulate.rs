use crate::simulation::info::Info;
use crate::simulation::{Event, EventKind, InfoKind, Simulation};
use crate::train_lines::{Direction, StationId, Time, TrainId};
use crate::utils::time::from_seconds;
use rand::Rng;

impl Simulation {
    pub fn simulation_step(&mut self) -> Result<Info, String> {
        let Event {
            time,
            kind: event_kind,
        } = self.events.pop().unwrap();

        let info_kind = match event_kind {
            EventKind::Start => {
                for id in self.trains.keys() {
                    self.events.push(Event {
                        time: 0.0,
                        kind: EventKind::TrainDepart(*id),
                    });
                }

                self.events.push(Event {
                    time: time + from_seconds(5.0),
                    kind: EventKind::PersonArrive(
                        rand::rng().random_range(0..self.graph.get_nodes_len()),
                    ),
                });

                InfoKind::SimulationStarted()
            }
            EventKind::End => InfoKind::SimulationEnded(),
            EventKind::TrainArrive(train_id) => {
                let (new_event, info) = self.train_arrive(time, train_id)?;
                self.events.push(new_event);
                info
            }
            EventKind::TrainDepart(train_id) => {
                let (new_event, info) = self.train_depart(time, train_id)?;
                self.events.push(new_event);
                info
            }
            EventKind::PersonArrive(station_id) => {
                let (new_event, info) = self.person_arrive(time, station_id)?;
                self.events.push(new_event);
                info
            }
        };

        Ok(Info {
            time,
            kind: info_kind,
        })
    }

    fn person_arrive(
        &mut self,
        time: Time,
        station_id: StationId,
    ) -> Result<(Event, InfoKind), String> {
        let n_stations = self.graph.get_nodes_len();
        let station = self
            .graph
            .get_node_mut(station_id)
            .ok_or("Station does not exist")?;
        let line_stop = station
            .get_random_line_stop()
            .ok_or("Station has no line stops")?;
        let direction = Direction::rand();
        line_stop.borrow_mut().person_enter(direction, 1);

        if self.next_train_id == 0 {
            return Err("No Train".to_string());
        }

        Ok((
            Event {
                time: time + from_seconds(5.0),
                kind: EventKind::PersonArrive(rand::rng().random_range(0..n_stations)),
            },
            InfoKind::PersonArrived {
                station_name: station.get_name(),
                line_name: line_stop.borrow().get_line_name(),
                direction,
            },
        ))
    }

    fn train_arrive(&mut self, time: Time, train_id: TrainId) -> Result<(Event, InfoKind), String> {
        let train = self
            .trains
            .get_mut(&train_id)
            .ok_or("Train does not exist")?;

        let start = train.get_curr_station();
        let (end, _) = train.get_next_station();

        let arrival_time = if start == end {
            // TODO not use 1
            time + 1.0
        } else {
            let curr_station = self.graph.get_node_mut(end).ok_or("Station not found")?;
            curr_station.train_enter();

            let edge = self
                .graph
                .get_edge_mut(start, end)
                .ok_or("Edge not found")?;
            edge.train_exit()
                .map_err(|()| "Cannot remove train because already 0 on edge")?;

            time + edge.get_distance()
        };

        train.go_next_stop();
        let curr_station = self.graph.get_node(end).ok_or("Station not found")?;
        train.unload_people_at_curr_station(curr_station);

        Ok((
            Event {
                time: arrival_time,
                kind: EventKind::TrainDepart(train_id),
            },
            InfoKind::TrainArrival {
                train_id,
                line_name: train.get_line_name(),
                arriving_station_name: curr_station.get_name(),
            },
        ))
    }

    fn train_depart(&mut self, time: Time, train_id: TrainId) -> Result<(Event, InfoKind), String> {
        let train = self
            .trains
            .get_mut(&train_id)
            .ok_or("Train does not exist")?;

        let start = train.get_curr_station();
        let (end, _) = train.get_next_station();

        train.load_people_at_curr_station()?;

        let arrival_time = if start == end {
            // TODO not use 1
            time + 1.0
        } else {
            let curr_station = self
                .graph
                .get_node_mut(start)
                .ok_or("Current station doesn't exist")?;

            curr_station
                .train_exit()
                .map_err(|()| "Cannot remove train because already 0 on node")?;

            let edge = self
                .graph
                .get_edge_mut(start, end)
                .ok_or("Edge doesn't exist")?;
            edge.train_enter();
            time + edge.get_distance()
        };

        let curr_station = self.graph.get_node(end).ok_or("Station not found")?;

        Ok((
            Event {
                time: arrival_time,
                kind: EventKind::TrainArrive(train_id),
            },
            InfoKind::TrainDeparture {
                train_id,
                line_name: train.get_line_name(),
                departing_station_name: curr_station.get_name(),
            },
        ))
    }
}
