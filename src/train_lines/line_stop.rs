use crate::train_lines::person::Person;
use crate::train_lines::{Direction, StationId};
use std::cell::RefCell;
use std::cmp::min;
use std::collections::VecDeque;
use std::fmt::Debug;
use std::rc::Rc;

pub struct LineStop {
    station_id: StationId,
    line_name: String,
    people_going_left: VecDeque<Person>,
    people_going_right: VecDeque<Person>,
}

impl LineStop {
    pub(crate) fn new(line_name: String, station_id: StationId) -> Rc<RefCell<Self>> {
        Rc::new(RefCell::new(Self {
            station_id,
            line_name,
            people_going_left: VecDeque::new(),
            people_going_right: VecDeque::new(),
        }))
    }

    fn get_mut_platform(&mut self, dir: Direction) -> &mut VecDeque<Person> {
        match dir {
            Direction::Left => &mut self.people_going_left,
            Direction::Right => &mut self.people_going_right,
        }
    }

    pub fn person_enter(&mut self, dir: Direction, person: Person) {
        let platform = self.get_mut_platform(dir);
        platform.push_back(person);
    }

    // Train may want to take up to n people
    pub fn person_exit(&mut self, dir: Direction, n: usize) -> Vec<Person> {
        let platform = self.get_mut_platform(dir);
        let n_to_exit = min(platform.len(), n);
        platform.drain(0..n_to_exit).collect()
    }

    pub fn get_people_on_platform(&self, dir: Direction) -> usize {
        match dir {
            Direction::Left => self.people_going_left.len(),
            Direction::Right => self.people_going_right.len(),
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
            "{}, {:?}, {:?}",
            self.station_id, self.people_going_left, self.people_going_right
        )
    }
}
