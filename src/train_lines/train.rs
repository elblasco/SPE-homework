use crate::graph::node::Station;
use crate::train_lines::line::Line;
use crate::train_lines::{Direction, StationId};
use rand::Rng;
use rand_distr::Distribution;
use rand_distr::Normal;
use std::rc::Rc;

#[derive(Debug)]
pub struct Train {
    n_passenger: usize,
    max_passenger: usize,
    line: Rc<Line>,
    pos_in_line: usize,
    direction: Direction,
    speed_distribution: Normal<f64>,
}

impl Train {
    // The average speed is 32.5 km/h accordin to:
    // https://homepage.univie.ac.at/horst.prillinger/ubahn/english/facts.html
    const AVERAGE_SPEED_MS: f64 = 32.5;

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
            speed_distribution: Normal::new(Self::AVERAGE_SPEED_MS, 1.0).unwrap(),
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

    pub fn go_next_stop(&mut self) {
        let (next_pos, next_dir) = self.get_next_position();
        self.pos_in_line = next_pos;
        self.direction = next_dir;
    }

    pub fn load_people_at_curr_station(&mut self) -> Result<usize, String> {
        let line_stop = self
            .line
            .get_stop(self.pos_in_line)
            .ok_or("Train's line stop does not exist")?;

        let n_people = line_stop
            .borrow_mut()
            .person_exit(self.direction, self.max_passenger - self.n_passenger);
        self.n_passenger += n_people;
        // assert!(self.n_passenger <= self.max_passenger);
        Ok(n_people)
    }

    pub fn unload_people_at_curr_station(&mut self, station: &Station) -> usize {
        let n_people = rand::rng().random_range(0..=self.n_passenger);
        self.n_passenger -= n_people;

        for _ in 0..n_people {
            if let Some(random_stop) = station.get_random_line_stop() {
                random_stop.borrow_mut().person_enter(Direction::rand(), 1);
            }
        }
        n_people
    }

    pub fn get_line_name(&self) -> String {
        self.line.get_name()
    }

    pub fn get_n_passengers(&self) -> usize {
        self.n_passenger
    }

    pub fn get_max_passenger(&self) -> usize {
        self.max_passenger
    }

    pub fn get_speed_m_s(&self) -> f64 {
        self.speed_distribution.sample(&mut rand::rng())
    }
}
