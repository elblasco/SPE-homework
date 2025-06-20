use crate::train_lines::Time;

#[derive(Debug, Default)]
pub struct Station {
    occupancy: usize,
}

impl Station {
    pub const fn train_enter(&mut self) {
        self.occupancy += 1;
    }

    pub const fn train_exit(&mut self) {
        self.occupancy -= 1;
    }
}

pub struct Edge {
    occupancy: usize,
    capacity: usize,
    distance: Time,
}

impl Edge {
    pub const fn new() -> Self {
        Self {
            occupancy: 0,
            capacity: 1,
            distance: 100, // TODO
        }
    }

    pub const fn train_enter(&mut self) -> Result<(), ()> {
        if self.occupancy < self.capacity {
            self.occupancy += 1;
            return Ok(());
        }
        Err(())
    }

    pub const fn train_exit(&mut self) -> Result<(), ()> {
        if self.occupancy > 0 {
            self.occupancy -= 1;
            return Ok(());
        }
        Err(())
    }

    pub const fn get_distance(&self) -> Time {
        self.distance
    }
}
