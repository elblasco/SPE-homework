use crate::graph::node::Station;
use crate::train_lines::line::Line;
use crate::train_lines::person::Person;
use crate::train_lines::{Direction, StationId, Time};
use rand::Rng;
use rand::seq::SliceRandom;
use rand_distr::Distribution;
use rand_distr::Normal;
use std::rc::Rc;

#[derive(Debug)]
pub struct Train {
    passengers: Vec<Person>,
    max_passengers: usize,
    line: Rc<Line>,
    pos_in_line: usize,
    direction: Direction,
    speed_distribution: Normal<f64>,
    depart_time: Time,
}

impl Train {
    // The average speed is 32.5 km/h accordin to:
    // https://homepage.univie.ac.at/horst.prillinger/ubahn/english/facts.html
    pub const AVG_SPEED_M_S: f64 = 30.0 / 3.6;
    pub const MAX_SPEED_M_S: f64 = 50.0 / 3.6;
    pub const MIN_SPEED_M_S: f64 = 10.0 / 3.6;

    pub fn new(
        line: Rc<Line>,
        max_passengers: usize,
        pos_in_line: usize,
        direction: Direction,
    ) -> Result<Self, String> {
        line.get(pos_in_line).ok_or("Invalid position in line")?;

        Ok(Self {
            passengers: vec![],
            max_passengers,
            line,
            pos_in_line,
            direction,
            speed_distribution: Normal::new(Self::AVG_SPEED_M_S, 0.5).unwrap(),
            depart_time: 0.0,
        })
    }

    pub fn get_curr_station(&self) -> StationId {
        self.line.get(self.pos_in_line).unwrap()
    }

    pub fn get_next_station(&self) -> (StationId, Direction) {
        self.line
            .get_next(self.pos_in_line, self.direction)
            .map(|next_station| (next_station, self.direction))
            .unwrap_or_else(|_| (self.get_curr_station(), self.direction.reverse()))
    }

    fn get_next_position(&self) -> (usize, Direction) {
        self.line
            .get_next_pos(self.pos_in_line, self.direction)
            .map(|next_pos| (next_pos, self.direction))
            .unwrap_or_else(|| (self.pos_in_line, self.direction.reverse()))
    }

    fn is_next_dir_changing(&self) -> bool {
        self.get_next_position().1 != self.direction
    }

    pub fn go_next_stop(&mut self) {
        let (next_pos, next_dir) = self.get_next_position();
        self.pos_in_line = next_pos;
        self.direction = next_dir;
    }

    // Returns number of people loaded at current station
    pub fn load_people_at_curr_station(&mut self, time: Time) -> Result<usize, String> {
        let line_stop = self
            .line
            .get_stop(self.pos_in_line)
            .ok_or("Train's line stop does not exist")?;

        let mut people = line_stop.borrow_mut().person_exit(
            self.direction,
            self.max_passengers - self.get_n_passengers(),
        );

        for p in &mut people {
            p.record_board(time, Rc::clone(&self.line), self.get_curr_station());
        }

        let n_people = people.len();
        self.passengers.extend(people);
        assert!(self.get_n_passengers() <= self.max_passengers);
        Ok(n_people)
    }

    // Returns number of people unloaded at current station
    // Also return the people that completely left the system
    pub fn unload_people_at_curr_station(
        &mut self,
        station: &Station,
        time: Time,
    ) -> Result<(usize, Vec<Person>), String> {
        let mut rng = rand::rng();

        let n_people = if self.is_next_dir_changing() {
            self.get_n_passengers()
        } else {
            rng.random_range(0..=self.get_n_passengers())
        };

        self.passengers.shuffle(&mut rng);
        let mut unloaded_people = self.passengers.drain(0..n_people).collect::<Vec<_>>();

        for p in &mut unloaded_people {
            // TODO CHECK station vs curr_station
            p.record_dismount(time, self.get_curr_station())?;
        }

        let total_decending = unloaded_people.len();
        let people_exited = station.deploy_people(unloaded_people, &self.line);
        Ok((total_decending, people_exited))
    }

    pub fn get_line_name(&self) -> String {
        self.line.get_name()
    }

    pub fn get_n_passengers(&self) -> usize {
        self.passengers.len()
    }

    pub fn get_max_passenger(&self) -> usize {
        self.max_passengers
    }

    pub fn get_speed_m_s(&self) -> f64 {
        self.speed_distribution
            .sample(&mut rand::rng())
            .clamp(Self::MIN_SPEED_M_S, Self::MAX_SPEED_M_S)
    }

    pub fn set_depart_time(&mut self, depart_time: Time) {
        self.depart_time = depart_time;
    }

    pub fn get_depart_time(&self) -> Time {
        self.depart_time
    }
}
