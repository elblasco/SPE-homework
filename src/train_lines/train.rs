use crate::train_lines::{Direction, StationId, TrainLine};
use std::rc::Rc;

pub struct Train {
    n_passenger: usize,
    max_passenger: usize,

    line: Rc<TrainLine>,
    pos_in_line: usize,
    direction: Direction,
    // status: Status,
}

impl Train {}

impl Train {
    pub const fn new(line: Rc<TrainLine>, max_passenger: usize) -> Self {
        Self {
            n_passenger: 0,
            max_passenger,
            line,
            pos_in_line: 0usize,         // TODO
            direction: Direction::Right, // TODO
        }
    }

    pub fn get_curr_station(&self) -> StationId {
        self.line.get(self.pos_in_line).unwrap()
    }

    pub fn get_next_station(&self) -> (StationId, Direction) {
        let next_station = self.line.get_next(self.pos_in_line, self.direction);
        if let Some(next_station) = next_station {
            return (next_station, self.direction);
        }

        (self.get_curr_station(), self.direction.reverse())
    }

    fn get_next_position(&self) -> (usize, Direction) {
        let next_station = self.line.get_next_pos(self.pos_in_line, self.direction);
        if let Some(next_station) = next_station {
            return (next_station, self.direction);
        }

        (self.pos_in_line, self.direction.reverse())
    }

    pub fn go_next_stop(&mut self) {
        let (next_pos, next_dir) = self.get_next_position();
        self.pos_in_line = next_pos;
        self.direction = next_dir;
    }
}
