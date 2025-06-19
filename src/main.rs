#![warn(clippy::pedantic)]
#![warn(clippy::nursery)]
#![warn(clippy::cargo)]
#![allow(clippy::cargo_common_metadata)]

use crate::simulation::TrainSystem;
use crate::train_lines::TrainLine;

mod simulation;
mod train_lines;

fn main() {
    println!("Hello, world!");
    let mut system = TrainSystem::new();
    let line = TrainLine::new(vec![1, 2, 3, 4, 5]);
    let line = system.add_line(line);
    system.add_train(3, 3, &line).unwrap();
    system.add_train(5, 4, &line).unwrap();
}
