use crate::dataset::LineData;
use crate::simulation::Simulation;
use crate::train_lines::TrainId;
use crate::train_lines::train::Train;
use crate::train_lines::train_line::{Direction, TrainLine};
use itertools::Itertools;
use std::rc::Rc;

impl Simulation {
    pub fn add_line(&mut self, line_data: &LineData) -> Rc<TrainLine> {
        let line = Rc::new(TrainLine::new(line_data.stops.clone()));
        self.lines.push(Rc::clone(&line));

        for (a, b) in line.iter_station_id().tuple_windows() {
            self.graph.add_edge(a, b);
            self.graph.add_edge(b, a);
        }

        for stop in line.iter() {
            let station_id = stop.borrow().get_station_id();
            let node = self.graph.get_node_mut(station_id).unwrap();
            node.add_line_stop(Rc::clone(stop));
        }

        line
    }

    pub fn add_train(
        &mut self,
        capacity: usize,
        line: &Rc<TrainLine>,
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
