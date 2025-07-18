#![warn(clippy::pedantic)]
#![warn(clippy::nursery)]
#![warn(clippy::cargo)]
#![allow(clippy::cargo_common_metadata)]
#![allow(clippy::missing_const_for_fn)]
#![allow(clippy::map_unwrap_or)]

use crate::dataset::Dataset;
use crate::simulation::{InfoKind, Simulation};
use crate::train_lines::line::Line;
use crate::train_lines::{Direction, Time};
use crate::utils::time::{fmt_time, from_days, from_hour};
use rand::Rng;
use std::fs::File;
use std::rc::Rc;

mod dataset;
mod graph;
mod logger;
mod simulation;
mod train_lines;
mod utils;

fn add_test_train(
    system: &mut Simulation,
    lines: &Vec<Rc<Line>>,
    n_trains_per_line: usize,
    max_capacity: usize,
) -> Result<(), String> {
    let mut rng = rand::rng();

    for line in lines {
        let line_len = line.iter().count();

        for _ in 0..n_trains_per_line {
            let capacity = rng.random_range(0..max_capacity);
            let pos = rng.random_range(0..line_len);
            system.add_train(capacity, line, pos, Direction::rand())?;
        }
    }

    Ok(())
}

const WARMUP_TIME: Time = from_days(100.0);
const SIM_LEN: Time = from_days(10.0);
const PRINT_INTERVAL: Time = from_hour(2.0);

fn main() {
    let file = File::open("datasets/Wien.json").expect("Cannot open file");
    let dataset =
        serde_json::from_reader::<File, Dataset>(file).expect("JSON was not well-formatted");

    let mut system = Simulation::new(-WARMUP_TIME, SIM_LEN, &dataset.stations);

    let mut lines = vec![];
    for data in &dataset.lines {
        let new_line = system.add_line(data).expect("Cannot create line");
        lines.push(new_line);
    }

    add_test_train(&mut system, &lines, 5, 200).unwrap();
    simulate(system);
}

fn simulate(mut system: Simulation) {
    let mut running = true;
    let mut last_printed_time = f64::MIN;

    println!();
    while running {
        let result = system.simulation_step();

        match result {
            Ok(info) => {
                if system.get_last_event_time() > last_printed_time + PRINT_INTERVAL {
                    last_printed_time = system.get_last_event_time();
                    if last_printed_time < 0.0 {
                        println!("Missing warmup time: {}", fmt_time(-last_printed_time));
                    } else {
                        println!("Currently at time: {}", fmt_time(last_printed_time));
                    }
                }

                #[cfg(debug_assertions)]
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

    system.flush_files();
}
