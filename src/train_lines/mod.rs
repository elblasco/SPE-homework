use rand::Rng;

pub mod line;
pub mod line_stop;
pub mod train;

pub type StationId = usize;
pub type TrainId = u32;
pub type LineId = u32;
pub type Time = f64;

#[derive(Debug, Eq, PartialEq, Copy, Clone)]
pub enum Direction {
    Left,
    Right,
}

impl Direction {
    pub fn reverse(self) -> Self {
        match self {
            Self::Left => Self::Right,
            Self::Right => Self::Left,
        }
    }

    pub fn rand() -> Self {
        if rand::rng().random_bool(0.5) {
            Self::Left
        } else {
            Self::Right
        }
    }
}
