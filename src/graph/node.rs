use crate::train_lines::Direction;
use crate::train_lines::line::Line;
use crate::train_lines::line_stop::LineStop;
use rand::Rng;
use rand::prelude::SliceRandom;
use rand_distr::Distribution;
use rand_distr::Exp;
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
pub struct Station {
    occupancy: usize,
    line_stops: Vec<Rc<RefCell<LineStop>>>,
    name: String,
    lat: f64,
    lon: f64,
    distribution_arrive: Exp<f64>,
}

impl Station {
    pub fn new(name: &str, lat: f64, lon: f64, mean: f64) -> Self {
        Self {
            occupancy: 0,
            line_stops: Vec::default(),
            name: String::from(name),
            lat,
            lon,
            distribution_arrive: Exp::new(1.0 / mean).unwrap(),
        }
    }

    pub fn get_name(&self) -> String {
        self.name.clone()
    }

    pub fn get_lat(&self) -> f64 {
        self.lat
    }

    pub fn get_lon(&self) -> f64 {
        self.lon
    }

    pub fn train_enter(&mut self) {
        self.occupancy += 1;
    }

    pub fn train_exit(&mut self) -> Result<usize, String> {
        if self.occupancy > 0 {
            self.occupancy -= 1;
            return Ok(self.occupancy);
        }
        Err("Station empty".to_string())
    }

    pub fn get_random_line_stop(&self) -> Result<Rc<RefCell<LineStop>>, String> {
        let rand = rand::rng().random_range(0..self.line_stops.len());

        self.line_stops
            .get(rand)
            .map(Rc::clone)
            .ok_or_else(|| "There is no next line stop".to_string())
    }

    //n_people: poeple descent from metro
    pub fn deploy_people(&self, n_people: usize, descending_from: &Rc<Line>) {
        if self.line_stops.len() <= 1 {
            // All people get out of the metro
            // TODO change rate of descent
            return;
        }
        let mut people_not_exited = rand::random_range(0..=n_people);
        let mut stops = self.line_stops.clone();
        stops.shuffle(&mut rand::rng());
        for stop in stops {
            if stop.borrow().get_line_name() == descending_from.get_name() {
                continue;
            }

            let people_for_curr_stop = rand::random_range(0..=people_not_exited);
            people_not_exited -= people_for_curr_stop;
            if people_for_curr_stop > 0 {
                stop.borrow_mut()
                    .person_enter(Direction::rand(), people_for_curr_stop);
            }
        }
    }

    pub fn add_line_stop(&mut self, new_train_line: Rc<RefCell<LineStop>>) {
        self.line_stops.push(new_train_line);
    }

    pub fn get_next_time(&self, current_time: f64) -> f64 {
        current_time + self.distribution_arrive.sample(&mut rand::rng())
    }

    // pub fn get_n_people(&self) -> usize {
    //     self.line_stops
    //         .iter()
    //         .map(|line_stop| {
    //             line_stop.borrow().get_people_on_platform(Direction::Left)
    //                 + line_stop.borrow().get_people_on_platform(Direction::Right)
    //         })
    //         .sum()
    // }
}
