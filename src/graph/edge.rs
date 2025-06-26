#[derive(Debug)]
pub struct Edge {
    occupancy: usize,
    // TODO add capacity
    distance: f64,
}

impl Edge {
    pub fn new(distance: f64) -> Self {
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

    pub fn get_distance_m(&self) -> f64 {
        self.distance
    }
}
