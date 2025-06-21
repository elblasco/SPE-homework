use crate::train_lines::Time;

#[derive(Debug)]
pub struct Edge {
    occupancy: usize,
    // TODO readd capacity
    // capacity: usize,
    distance: Time,
}

impl Edge {
    pub fn new() -> Self {
        Self {
            occupancy: 0,
            // capacity: 1,
            distance: 100, // TODO
        }
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

    pub fn get_distance(&self) -> Time {
        self.distance
    }
}
