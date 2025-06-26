use crate::train_lines::line_stop::LineStop;
use rand::Rng;
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

    pub fn train_exit(&mut self) -> Result<usize, ()> {
        if self.occupancy > 0 {
            self.occupancy -= 1;
            return Ok(self.occupancy);
        }
        Err(())
    }

    pub fn get_random_line_stop(&self) -> Option<Rc<RefCell<LineStop>>> {
        if self.line_stops.is_empty() {
            return None;
        }

        let rand = rand::rng().random_range(0..self.line_stops.len());
        self.line_stops.get(rand).map(Rc::clone)
    }

    pub fn add_line_stop(&mut self, new_train_line: Rc<RefCell<LineStop>>) {
        self.line_stops.push(new_train_line);
    }

    pub fn get_next_time(&self, current_time: f64) -> f64 {
        current_time + self.distribution_arrive.sample(&mut rand::rng())
    }
}
