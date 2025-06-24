use crate::train_lines::Time;

#[derive(Debug)]
pub struct Edge {
    occupancy: usize,
    // TODO add capacity
    distance: Time,
}

impl Edge {
    pub fn new(distance: Time) -> Self {
        Self {
            occupancy: 0,
            distance,
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
