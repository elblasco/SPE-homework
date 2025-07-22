use crate::dataset::LineData;
use crate::simulation::Simulation;
use crate::train_lines::line::Line;
use crate::train_lines::train::Train;
use crate::train_lines::{Direction, TrainId};
use itertools::Itertools;
use rand::distr::Distribution;
use std::rc::Rc;

const EDGE_MAX_CAPACITY: usize = 1;

impl Simulation {
    pub fn add_line(&mut self, line_data: &LineData) -> Result<Rc<Line>, String> {
        let line = Rc::new(Line::new(line_data.name.clone(), line_data.stops.clone()));
        self.lines.push(Rc::clone(&line));

        //println!("{}", line_data.name);
        for (a, b) in line.iter_station_id().tuple_windows() {
            let node_a = self.graph.get_node(a)?;
            //let name_a = node_a.get_name();
            let node_b = self.graph.get_node(b)?;
            //let name_b = node_b.get_name();

            let distance_m = haversine(
                node_a.get_lat(),
                node_a.get_lon(),
                node_b.get_lat(),
                node_b.get_lon(),
            );

            self.graph.add_edge(a, b, distance_m, EDGE_MAX_CAPACITY);
            self.graph.add_edge(b, a, distance_m, EDGE_MAX_CAPACITY);
            // println!(
            //     "{name_a} -> {name_b} distance {distance_m:.02} m traveled in {} s",
            //     fmt_time(time_distance)
            // );
        }

        for stop in line.iter() {
            let station_id = stop.borrow().get_station_id();
            let node = self.graph.get_node_mut(station_id)?;
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
        let station = self.graph.get_node_mut(station_id)?;
        let m_before_crash = self.distr_m_before_crash.sample(&mut rand::rng());

        let _ = self.trains.insert(
            self.next_train_id,
            Train::new(Rc::clone(line), capacity, pos_in_line, dir, m_before_crash)?,
        );
        station.train_enter();
        self.next_train_id += 1;

        Ok(self.next_train_id - 1)
    }
}

// Distance (meters) between two points (latitude and longitude in radians)
fn haversine(lat1_deg: f64, lon1_deg: f64, lat2_deg: f64, lon2_deg: f64) -> f64 {
    const EARTH_RADIUS: f64 = 6_371_008.771_4;
    const DEG_TO_RAD: f64 = std::f64::consts::PI / 180.0;

    // Convert degrees to radians
    let lat1 = lat1_deg * DEG_TO_RAD;
    let lon1 = lon1_deg * DEG_TO_RAD;
    let lat2 = lat2_deg * DEG_TO_RAD;
    let lon2 = lon2_deg * DEG_TO_RAD;

    let a = ((lat2 - lat1) / 2.0).sin().mul_add(
        ((lat2 - lat1) / 2.0).sin(),
        lat1.cos() * lat2.cos() * ((lon2 - lon1) / 2.0).sin().powi(2),
    );
    2.0 * EARTH_RADIUS * a.sqrt().asin()
}
