#![warn(clippy::pedantic)]
#![warn(clippy::nursery)]
#![warn(clippy::cargo)]
#![allow(clippy::cargo_common_metadata)]
#![allow(dead_code)]

use crate::simulation::Simulation;
use crate::train_lines::train_line::{Direction, TrainLine};

mod graph;
mod simulation;
mod train_lines;

fn main() {
    println!("Hello, world!");
    let mut system = Simulation::new(0, 1000);
    let line = TrainLine::new(vec![1, 2, 3, 4, 5]);
    let line = system.add_line(line);
    system.add_train(3, &line, 2, Direction::Left).unwrap();
    system.add_train(5, &line, 3, Direction::Right).unwrap();

    let mut running = true;
    while running {
        println!("{:?}", system.peek_event());
        match system.simulation_step() {
            Ok(status) => running = !status,
            Err(error) => {
                println!("Simulation errored out");
                println!("{}", error);
                println!();
                println!("{:?}", system);
                running = false;
            }
        }
    }
}
