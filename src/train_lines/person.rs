use crate::train_lines::line::Line;
use crate::train_lines::{StationId, Time};
use std::rc::Rc;

#[derive(Debug)]
pub struct Person {
    arrival_time: Time,
    steps: Vec<Step>,
    final_station_id: Option<StationId>,
}

#[derive(Debug)]
pub struct Step {
    line_name: Rc<Line>,
    from_station_id: StationId,
    board_time: Time,
    // Initially equals to board time
    dismount_time: Time,
}

impl Person {
    pub fn new(arrival_time: Time) -> Self {
        Self {
            arrival_time,
            steps: vec![],
            final_station_id: None,
        }
    }

    pub fn record_board(&mut self, time: Time, line: Rc<Line>, from: StationId) {
        self.steps.push(Step {
            line_name: line,
            from_station_id: from,
            board_time: time,
            dismount_time: time,
        });
    }

    pub fn record_dismount(
        &mut self,
        time: Time,
        arriving_station_id: StationId,
    ) -> Result<(), String> {
        let last = self
            .steps
            .last_mut()
            .ok_or("Cannot dismount person who never boarded")?;
        last.dismount_time = time;
        self.final_station_id = Some(arriving_station_id);
        Ok(())
    }

    pub fn get_arrival_time(&self) -> Time {
        self.arrival_time
    }

    pub fn iter_steps(&self) -> impl Iterator<Item = &Step> {
        self.steps.iter()
    }
}

impl Step {
    pub fn get_line_name(&self) -> String {
        self.line_name.get_name()
    }

    pub fn get_from_station_id(&self) -> StationId {
        self.from_station_id
    }

    pub fn get_board_time(&self) -> Time {
        self.board_time
    }

    pub fn get_dismount_time(&self) -> Time {
        self.dismount_time
    }
}
