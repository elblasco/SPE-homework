use crate::train_lines::train_line::LineStop;
use rand::Rng;
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
pub struct Station {
    occupancy: usize,
    line_stops: Vec<Rc<RefCell<LineStop>>>,
}

impl Station {
    pub fn new(line_stops: Vec<Rc<RefCell<LineStop>>>) -> Self {
        Self {
            occupancy: 0,
            line_stops,
        }
    }

    pub const fn train_enter(&mut self) {
        self.occupancy += 1;
    }

    pub const fn train_exit(&mut self) -> Result<usize, ()> {
        if self.occupancy > 0 {
            self.occupancy -= 1;
            return Ok(self.occupancy);
        }
        Err(())
    }

    pub fn get_random_line_stop_mut(&mut self) -> Option<Rc<RefCell<LineStop>>> {
        if self.line_stops.is_empty() {
            return None;
        }

        let rand = rand::rng().random_range(0..self.line_stops.len());
        self.line_stops.get(rand).map(Rc::clone)
    }
}
