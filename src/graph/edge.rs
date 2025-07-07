#[derive(Debug)]
pub struct Edge {
    occupancy: usize,
    max_capacity: usize,
    distance: f64,
}

impl Edge {
    pub fn new(distance: f64, max_capacity: usize) -> Self {
        Self {
            occupancy: 0,
            max_capacity,
            distance,
        }
    }

    pub fn has_free_space(&self) -> bool {
        self.occupancy < self.max_capacity
    }

    pub fn train_enter(&mut self) -> Result<usize, String> {
        if self.occupancy < self.max_capacity {
            self.occupancy += 1;
            return Ok(self.occupancy);
        }
        Err("Edge capacity exceeded".to_string())
    }

    pub fn train_exit(&mut self) -> Result<usize, String> {
        if self.occupancy > 0 {
            self.occupancy -= 1;
            return Ok(self.occupancy);
        }
        Err("Edge already empty".to_string())
    }

    pub fn get_distance_m(&self) -> f64 {
        self.distance
    }
}
