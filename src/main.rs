#![warn(clippy::pedantic)]
#![warn(clippy::nursery)]
#![warn(clippy::cargo)]
#![allow(clippy::cargo_common_metadata)]
#![allow(clippy::missing_const_for_fn)]
#![allow(clippy::map_unwrap_or)]

use crate::dataset::Dataset;
use crate::simulation::{InfoKind, Simulation};
use crate::train_lines::Direction::{Left, Right};
use crate::utils::time::{fmt_time, from_hour};
use std::fs::File;

mod dataset;
mod graph;
mod logger;
mod simulation;
mod train_lines;
mod utils;

fn main() {
    let file = File::open("datasets/Wien.json").expect("Cannot open file");
    let dataset =
        serde_json::from_reader::<File, Dataset>(file).expect("JSON was not well-formatted");

    let mut system = Simulation::new(0.0, from_hour(24.0), &dataset.stations);

    let mut lines = vec![];
    for data in &dataset.lines {
        let new_line = system.add_line(data).expect("Cannot create line");
        lines.push(new_line);
    }

    system.add_train(30, &lines[0], 2, Left).unwrap();
    system.add_train(50, &lines[1], 3, Right).unwrap();
    system.add_train(70, &lines[1], 2, Right).unwrap();
    system.add_train(70, &lines[1], 2, Right).unwrap();

    simulate(system);
}

fn simulate(mut system: Simulation) {
    let mut running = true;

    println!();
    while running {
        let result = system.simulation_step();

        match result {
            Ok(info) => {
                match info.kind {
                    InfoKind::PersonArrived { .. } | InfoKind::TimedSnapshot { .. } => {}
                    _ => {
                        println!("LOG {} -> {}", fmt_time(info.time), info.kind);
                    }
                }
                running = !matches!(info.kind, InfoKind::SimulationEnded());
            }
            Err(error) => {
                println!("\n\nCORE DUMPED");
                println!("{:?}", system.iter_trains().collect::<Vec<_>>());
                println!("\n\nSIMULATION ERRORED OUT");
                println!("{error}");
                running = false;
            }
        }
    }
}
