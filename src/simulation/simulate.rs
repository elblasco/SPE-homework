use crate::simulation::event::SnapshotKind;
use crate::simulation::info::Info;
use crate::simulation::{Event, EventKind, InfoKind, Simulation};
use crate::train_lines::train::Train;
use crate::train_lines::{Direction, StationId, Time, TrainId};
use crate::utils::time::{from_minutes, from_seconds};
use rand_distr::Distribution;
use std::collections::VecDeque;
use std::io::Write;

impl Simulation {
    pub fn simulation_step(&mut self) -> Result<Info, String> {
        let Event {
            time,
            kind: event_kind,
        } = self.events.pop().unwrap();

        let info_kind = match event_kind {
            EventKind::Start => self.start_sim(time),
            EventKind::End => InfoKind::SimulationEnded(),
            EventKind::TrainArrive(train_id) => {
                let (new_event, info) = self.train_arrive(time, train_id)?;
                self.events.extend(new_event);
                info
            }
            EventKind::TrainDepart(train_id) => {
                let (new_event, info) = self.train_depart(time, train_id)?;
                if let Some(new_event) = new_event {
                    self.events.push(new_event);
                }
                info
            }
            EventKind::PersonArrive(station_id) => {
                let (new_event, info) = self.person_arrive(time, station_id)?;
                self.events.push(new_event);
                info
            }
            EventKind::TimedSnapshot(kind) => {
                let new_event = self.snapshot(time, kind.clone());
                self.events.push(new_event);
                InfoKind::TimedSnapshot(kind)
            }
        };

        Ok(Info {
            time,
            kind: info_kind,
        })
    }

    fn start_sim(&mut self, time: Time) -> InfoKind {
        for (id, train) in &mut self.trains {
            let depart_time = time + self.distr_train_at_station.sample(&mut rand::rng());

            train.set_depart_time(depart_time);

            self.events.push(Event {
                time: depart_time,
                kind: EventKind::TrainDepart(*id),
            });
        }

        self.events.push(Event {
            time: Self::TIME_BETWEEN_SNAPSHOT,
            kind: EventKind::TimedSnapshot(SnapshotKind::PeopleInStation),
        });

        let station_ids = self.graph.iter_station_id().copied().collect::<Vec<_>>();
        for station_id in station_ids {
            self.events.push(Event {
                time: self
                    .graph
                    .get_node_mut(station_id)
                    .unwrap()
                    .get_next_time(time),
                kind: EventKind::PersonArrive(station_id),
            });
        }

        InfoKind::SimulationStarted()
    }

    fn person_arrive(
        &mut self,
        time: Time,
        station_id: StationId,
    ) -> Result<(Event, InfoKind), String> {
        // let n_stations = self.graph.get_nodes_len();
        let station = self.graph.get_node_mut(station_id)?;
        let line_stop = station.get_random_line_stop()?;
        let direction = Direction::rand();
        line_stop.borrow_mut().person_enter(direction, 1);

        if self.next_train_id == 0 {
            return Err("No Train".to_string());
        }

        Ok((
            Event {
                time: station.get_next_time(time),
                kind: EventKind::PersonArrive(station_id),
            },
            InfoKind::PersonArrived {
                station_name: station.get_name(),
                line_name: line_stop.borrow().get_line_name(),
                direction,
            },
        ))
    }

    fn snapshot(&self, time: Time, snapshot_kind: SnapshotKind) -> Event {
        match snapshot_kind {
            SnapshotKind::PeopleInStation => {
                let mut tot = 0;
                for line in &self.lines {
                    let n_people = line.get_n_people();
                    tot += n_people;

                    writeln!(
                        &self.logger.people_in_stations,
                        "{time}, {n_people}, {}",
                        line.get_name()
                    )
                    .expect("Cannot write to log");
                }
                writeln!(&self.logger.people_in_stations, "{time}, {tot}, All lines")
                    .expect("Cannot write to log");
            }
        }

        Event {
            time: time + Self::TIME_BETWEEN_SNAPSHOT,
            kind: EventKind::TimedSnapshot(snapshot_kind),
        }
    }

    fn train_arrive(
        &mut self,
        time: Time,
        train_id: TrainId,
    ) -> Result<(Vec<Event>, InfoKind), String> {
        let train = self
            .trains
            .get_mut(&train_id)
            .ok_or("Train does not exist")?;

        let start = train.get_curr_station();
        let (end, _) = train.get_next_station();

        let departure_time = if start == end {
            time + from_minutes(1.0)
        } else {
            let curr_station = self.graph.get_node_mut(end)?;
            curr_station.train_enter();

            let edge = self.graph.get_edge_mut(start, end)?;
            edge.train_exit()
                .map_err(|err_str: String| format!("Cannot remove train because {err_str}"))?;

            time + self.distr_train_at_station.sample(&mut rand::rng())
        };

        train.go_next_stop();
        let arrival_station = self.graph.get_node(end)?;
        // TODO maybe we should do something with them
        let unloaded_passengers = train.unload_people_at_curr_station(arrival_station);

        let mut events = vec![Event {
            time: departure_time,
            kind: EventKind::TrainDepart(train_id),
        }];
        let train_freed = self
            .train_waiting
            .get_mut(&(start, end))
            .and_then(VecDeque::pop_front)
            .map(|train_id| Event {
                time,
                kind: EventKind::TrainDepart(train_id),
            });
        events.extend(train_freed);
        train.set_depart_time(departure_time);

        Ok((
            events,
            InfoKind::TrainArrival {
                train_id,
                line_name: train.get_line_name(),
                arriving_station_name: arrival_station.get_name(),
                unloaded_passengers,
                total_passengers: train.get_n_passengers(),
                train_capacity: train.get_max_passenger(),
            },
        ))
    }

    fn train_depart(
        &mut self,
        time: Time,
        train_id: TrainId,
    ) -> Result<(Option<Event>, InfoKind), String> {
        let train = self
            .trains
            .get_mut(&train_id)
            .ok_or("Train does not exist")?;

        let start = train.get_curr_station();
        let (end, _) = train.get_next_station();

        let loaded_passengers = train.load_people_at_curr_station()?;

        let arrival_time = if start == end {
            time + from_minutes(1.0)
        } else {
            let edge = self.graph.get_edge(start, end)?;

            if !edge.has_free_space() {
                let start_station = self.graph.get_node(start)?;

                let end_station = self.graph.get_node(end)?;

                self.train_waiting
                    .entry((start, end))
                    .or_default()
                    .push_back(train_id);

                return Ok((
                    None,
                    InfoKind::WaitingForEdge {
                        train_id,
                        start_station_name: start_station.get_name(),
                        end_station_name: end_station.get_name(),
                    },
                ));
            }

            let curr_station = self.graph.get_node_mut(start)?;

            curr_station
                .train_exit()
                .map_err(|err_str: String| format!("Cannot remove train because {err_str}"))?;

            let edge = self.graph.get_edge_mut(start, end)?;

            edge.train_enter()
                .map_err(|err_str: String| format!("Cannot instert train because {err_str}"))?;

            let arrival = time + from_seconds(edge.get_distance_m() / (train.get_speed_m_s()));
            writeln!(
                self.logger.delay,
                "{}, {}, {}",
                from_seconds(edge.get_distance_m() / Train::AVG_SPEED_M_S) * 3600.0,
                (arrival - train.get_depart_time()) * 3600.0,
                train.get_line_name()
            )
            .expect("Cannot write to log");
            arrival
        };

        let departure_station = self.graph.get_node(start)?;

        Ok((
            Some(Event {
                time: arrival_time,
                kind: EventKind::TrainArrive(train_id),
            }),
            InfoKind::TrainDeparture {
                train_id,
                line_name: train.get_line_name(),
                departing_station_name: departure_station.get_name(),
                total_passengers: train.get_n_passengers(),
                loaded_passengers,
                train_capacity: train.get_max_passenger(),
            },
        ))
    }
}
