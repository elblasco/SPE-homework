use crate::train_lines::StationId;
use std::slice::Iter;

#[derive(Debug, Eq, PartialEq, Copy, Clone)]
pub enum Direction {
    Left,
    Right,
}

impl Direction {
    pub(crate) fn reverse(self) -> Direction {
        match self {
            Direction::Left => Direction::Right,
            Direction::Right => Direction::Left,
        }
    }
}

pub struct TrainLine {
    stops: Vec<StationId>,
}

impl TrainLine {
    pub fn new(stops: Vec<StationId>) -> Self {
        Self { stops }
    }

    pub fn get(&self, pos: usize) -> Option<StationId> {
        Some(*self.stops.get(pos)?)
    }

    pub fn iter(&self) -> Iter<'_, StationId> {
        self.stops.iter()
    }

    pub fn get_next(&self, pos: usize, dir: Direction) -> Option<StationId> {
        match dir {
            Direction::Left => self.get(pos - 1),
            Direction::Right => self.get(pos + 1),
        }
    }
    pub fn get_next_pos(&self, pos: usize, dir: Direction) -> Option<usize> {
        let pos = match dir {
            Direction::Left => pos - 1,
            Direction::Right => pos + 1,
        };

        self.get(pos).map(|_| pos)
    }
}
