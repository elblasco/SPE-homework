use crate::graph::node::Station;
use crate::simulation::Simulation;
use crate::train_lines::train::Train;
use crate::train_lines::train_line::{Direction, TrainLine};
use crate::train_lines::TrainId;
use itertools::Itertools;
use std::rc::Rc;

impl Simulation {
    pub fn add_line(&mut self, line: TrainLine) -> Rc<TrainLine> {
        // TODO remove and use map instead

        for (a_pos, (a, b)) in line.iter().tuple_windows().enumerate() {
            self.graph.add_edge(a, b);
            self.graph.add_edge(b, a);
            self.graph.add_node(
                a,
                Station::new(vec![Rc::clone(line.get_stop(a_pos).unwrap())]),
            );
            self.graph.add_node(
                b,
                Station::new(vec![Rc::clone(line.get_stop(a_pos + 1).unwrap())]),
            );
        }

        let line = Rc::new(line);
        self.lines.push(Rc::clone(&line));

        line
    }

    pub fn add_train(
        &mut self,
        capacity: usize,
        line: &Rc<TrainLine>,
        pos_in_line: usize,
        dir: Direction,
    ) -> Result<TrainId, String> {
        let station_id = line.get(pos_in_line).ok_or_else(|| "Invalid pos in line")?;
        let station = self
            .graph
            .get_node_mut(station_id)
            .ok_or_else(|| "Line is broken, no station connected")?;

        let _ = self.trains.insert(
            self.next_train_id,
            Train::new(Rc::clone(line), capacity, pos_in_line, dir)
                .ok_or_else(|| "Invalid pos in line")?,
        );
        station.train_enter();
        self.next_train_id += 1;

        Ok(self.next_train_id - 1)
    }
}
