use crate::train_lines::line_stop::LineStop;
use crate::train_lines::{Direction, StationId};
use std::cell::RefCell;
use std::fmt::Debug;
use std::rc::Rc;

pub struct Line {
    name: String,
    stops: Vec<Rc<RefCell<LineStop>>>,
}

impl Line {
    pub fn new(name: String, stations: Vec<StationId>) -> Self {
        let stops = stations
            .into_iter()
            .map(|station_id| LineStop::new(name.clone(), station_id))
            .collect();
        Self { name, stops }
    }

    pub fn get(&self, pos: usize) -> Option<StationId> {
        Some(self.stops.get(pos)?.borrow().get_station_id())
    }

    pub fn iter_station_id(&self) -> impl Iterator<Item = StationId> {
        self.stops
            .iter()
            .map(|line_stop| line_stop.borrow().get_station_id())
    }

    pub fn iter(&self) -> impl Iterator<Item = &Rc<RefCell<LineStop>>> {
        self.stops.iter()
    }

    pub fn get_next(&self, pos: usize, dir: Direction) -> Option<StationId> {
        match dir {
            Direction::Left => self.get(pos.checked_sub(1)?),
            Direction::Right => self.get(pos + 1),
        }
    }
    pub fn get_next_pos(&self, pos: usize, dir: Direction) -> Option<usize> {
        let pos = match dir {
            Direction::Left => pos.checked_sub(1)?,
            Direction::Right => pos + 1,
        };

        self.get(pos).map(|_| pos)
    }

    pub fn get_stop(&self, pos: usize) -> Option<&Rc<RefCell<LineStop>>> {
        self.stops.get(pos)
    }

    pub fn get_name(&self) -> String {
        self.name.clone()
    }

    pub fn get_n_people(&self) -> usize {
        self.iter()
            .map(|line_stop| {
                line_stop.borrow().get_people_on_platform(Direction::Left)
                    + line_stop.borrow().get_people_on_platform(Direction::Right)
            })
            .sum()
    }
}

impl Debug for Line {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for stop in &self.stops {
            write!(f, "({:?}) ", stop.borrow())?;
        }
        Ok(())
    }
}
