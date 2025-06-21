use crate::train_lines::StationId;
use rand::Rng;
use std::cell::RefCell;
use std::cmp::min;
use std::fmt::Debug;
use std::rc::Rc;

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

pub struct LineStop {
    station_id: StationId,
    people_going_left: usize,
    people_going_right: usize,
}

impl LineStop {
    fn new(station_id: StationId) -> Rc<RefCell<Self>> {
        Rc::new(RefCell::new(Self {
            station_id,
            people_going_left: 0,
            people_going_right: 0,
        }))
    }

    fn get_mut_platform(&mut self, dir: Direction) -> &mut usize {
        match dir {
            Direction::Left => &mut self.people_going_left,
            Direction::Right => &mut self.people_going_right,
        }
    }

    pub fn person_enter(&mut self, dir: Direction, n: usize) -> usize {
        let platform = self.get_mut_platform(dir);
        *platform += n;
        n
    }

    // Train may want to take up to n people
    pub fn person_exit(&mut self, dir: Direction, n: usize) -> usize {
        let platform = self.get_mut_platform(dir);
        let n_to_exit = min(*platform, n);
        *platform -= n_to_exit;
        n_to_exit
    }

    pub fn get_people_on_platform(&self, dir: Direction) -> usize {
        match dir {
            Direction::Left => self.people_going_left,
            Direction::Right => self.people_going_right,
        }
    }
}

impl Debug for LineStop {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}, {}, {}",
            self.station_id, self.people_going_left, self.people_going_right
        )
    }
}

pub struct TrainLine {
    stops: Vec<Rc<RefCell<LineStop>>>,
}

impl TrainLine {
    pub fn new(stations: Vec<StationId>) -> Self {
        let stops = stations.into_iter().map(LineStop::new).collect();
        Self { stops }
    }

    pub fn get(&self, pos: usize) -> Option<StationId> {
        Some(self.stops.get(pos)?.borrow().station_id)
    }

    pub fn iter(&self) -> impl Iterator<Item = StationId> {
        self.stops
            .iter()
            .map(|line_stop| line_stop.borrow().station_id)
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

    pub fn person_enter(&self, pos: usize, dir: Direction, n: usize) -> Result<usize, ()> {
        let stop = self.stops.get(pos).ok_or(())?;
        Ok(stop.borrow_mut().person_enter(dir, n))
    }

    // Train may want to take up to n people
    pub fn person_exit(&self, pos: usize, dir: Direction, n: usize) -> Result<usize, ()> {
        let stop = self.stops.get(pos).ok_or(())?;
        Ok(stop.borrow_mut().person_exit(dir, n))
    }

    pub fn get_stop(&self, pos: usize) -> Option<&Rc<RefCell<LineStop>>> {
        self.stops.get(pos)
    }
}

impl Debug for TrainLine {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for stop in &self.stops {
            write!(f, "({:?}) ", stop.borrow())?;
        }
        Ok(())
    }
}
