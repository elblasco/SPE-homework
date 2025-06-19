#![allow(dead_code)]

mod graph_elements;
mod train;
mod train_line;

pub use graph_elements::{Station, *};
pub use train::Train;
pub use train_line::Direction;
pub use train_line::TrainLine;

pub type StationId = u32;
pub type TrainId = u32;
pub type LineId = u32;
pub type Time = u64;
