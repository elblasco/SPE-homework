use crate::dataset::LineData;
use crate::simulation::Simulation;
use crate::train_lines::line::Line;
use crate::train_lines::train::Train;
use crate::train_lines::{Direction, Time, TrainId};
use crate::utils::time::{fmt_time, from_seconds};
use itertools::Itertools;
use std::rc::Rc;

impl Simulation {
    pub fn add_line(&mut self, line_data: &LineData) -> Result<Rc<Line>, String> {
        let line = Rc::new(Line::new(line_data.name.clone(), line_data.stops.clone()));
        self.lines.push(Rc::clone(&line));

        println!("{}", line_data.name);
        for (a, b) in line.iter_station_id().tuple_windows() {
            let node_a = self.graph.get_node(a).ok_or("Missing station")?;
            let node_b = self.graph.get_node(b).ok_or("Missing station")?;

            let distance_m = haversine(
                node_a.get_lat(),
                node_a.get_lon(),
                node_b.get_lat(),
                node_b.get_lon(),
            );
            let time_distance: Time = from_seconds(distance_m / (300f64 / 3.6));

            self.graph.add_edge(a, b, time_distance);
            self.graph.add_edge(b, a, time_distance);
            println!("{}", fmt_time(time_distance));
        }

        for stop in line.iter() {
            let station_id = stop.borrow().get_station_id();
            let node = self.graph.get_node_mut(station_id).unwrap();
            node.add_line_stop(Rc::clone(stop));
        }

        Ok(line)
    }

    pub fn add_train(
        &mut self,
        capacity: usize,
        line: &Rc<Line>,
        pos_in_line: usize,
        dir: Direction,
    ) -> Result<TrainId, String> {
        let station_id = line.get(pos_in_line).ok_or("Invalid pos in line")?;
        let station = self
            .graph
            .get_node_mut(station_id)
            .ok_or("Line is broken, no station connected")?;

        let _ = self.trains.insert(
            self.next_train_id,
            Train::new(Rc::clone(line), capacity, pos_in_line, dir).ok_or("Invalid pos in line")?,
        );
        station.train_enter();
        self.next_train_id += 1;

        Ok(self.next_train_id - 1)
    }
}

// Distance (meters) between two points (latitude and longitude in radians)
fn haversine(lat1: f64, lon1: f64, lat2: f64, lon2: f64) -> f64 {
    const EARTH_RADIUS: f64 = 6_371_008.771_4;

    let a = ((lat2 - lat1) / 2.0).sin().mul_add(
        ((lat2 - lat1) / 2.0).sin(),
        lat1.cos() * lat2.cos() * ((lon2 - lon1) / 2.0).sin().powi(2),
    );
    2.0 * EARTH_RADIUS * a.sqrt().asin()
}
