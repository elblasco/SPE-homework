use crate::graph::node::Station;
use crate::train_lines::line::Line;
use crate::train_lines::{Direction, StationId};
use rand::Rng;
use std::rc::Rc;

#[derive(Debug)]
pub struct Train {
    n_passenger: usize,
    max_passenger: usize,

    line: Rc<Line>,
    pos_in_line: usize,
    direction: Direction,
}

impl Train {
    pub fn new(
        line: Rc<Line>,
        max_passenger: usize,
        pos_in_line: usize,
        direction: Direction,
    ) -> Option<Self> {
        line.get(pos_in_line)?;

        Some(Self {
            n_passenger: 0,
            max_passenger,
            line,
            pos_in_line,
            direction,
        })
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

    pub fn get_pos_in_line(&self) -> usize {
        self.pos_in_line
    }

    pub fn go_next_stop(&mut self) {
        let (next_pos, next_dir) = self.get_next_position();
        self.pos_in_line = next_pos;
        self.direction = next_dir;
    }

    pub fn load_people_at_curr_station(&mut self) -> Result<(), String> {
        let line_stop = self
            .line
            .get_stop(self.pos_in_line)
            .ok_or("Train's line stop does not exist")?;

        let n_people = line_stop
            .borrow_mut()
            .person_exit(self.direction, self.max_passenger - self.n_passenger);
        self.n_passenger += n_people;
        assert!(self.n_passenger <= self.max_passenger);
        Ok(())
    }

    pub fn unload_people_at_curr_station(&mut self, station: &Station) {
        let n_people = rand::rng().random_range(0..=self.n_passenger);
        self.n_passenger -= n_people;

        for _ in 0..n_people {
            if let Some(random_stop) = station.get_random_line_stop() {
                random_stop.borrow_mut().person_enter(Direction::rand(), 1);
            }
        }
    }

    pub fn get_line_name(&self) -> String {
        self.line.get_name()
    }
}
