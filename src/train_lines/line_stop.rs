use crate::train_lines::{Direction, StationId};
use std::cell::RefCell;
use std::cmp::min;
use std::fmt::Debug;
use std::rc::Rc;

pub struct LineStop {
    station_id: StationId,
    line_name: String,
    people_going_left: usize,
    people_going_right: usize,
}

impl LineStop {
    pub(crate) fn new(line_name: String, station_id: StationId) -> Rc<RefCell<Self>> {
        Rc::new(RefCell::new(Self {
            station_id,
            line_name,
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

    pub fn get_station_id(&self) -> StationId {
        self.station_id
    }

    pub fn get_line_name(&self) -> String {
        self.line_name.clone()
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
