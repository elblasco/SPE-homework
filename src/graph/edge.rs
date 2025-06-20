use crate::train_lines::Time;

#[derive(Debug)]
pub struct Edge {
    occupancy: usize,
    // TODO readd capacity
    // capacity: usize,
    distance: Time,
}

impl Edge {
    pub const fn new() -> Self {
        Self {
            occupancy: 0,
            // capacity: 1,
            distance: 100, // TODO
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

    pub const fn get_distance(&self) -> Time {
        self.distance
    }
}
