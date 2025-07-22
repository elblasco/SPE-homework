#![warn(clippy::pedantic)]
#![warn(clippy::nursery)]
#![warn(clippy::cargo)]
#![allow(clippy::cargo_common_metadata)]
#![allow(clippy::missing_const_for_fn)]
#![allow(clippy::map_unwrap_or)]

use crate::dataset::Dataset;
use crate::simulation::{InfoKind, Simulation};
use crate::train_lines::Direction;
use crate::train_lines::line::Line;
use crate::utils::config::{PRINT_INTERVAL, SIM_LEN, TRAIN_CAPACITY, TRAIN_PER_LINE, WARMUP_TIME};
use crate::utils::time::fmt_time;
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

fn main() {
    let file = File::open("datasets/Wien.json")
        .expect("Cannot open datasets file (running from wrong location?)");
    let dataset =
        serde_json::from_reader::<File, Dataset>(file).expect("JSON was not well-formatted");

    let mut system = Simulation::new(-WARMUP_TIME, SIM_LEN, &dataset.stations);

    let mut lines = vec![];
    for data in &dataset.lines {
        let new_line = system.add_line(data).expect("Cannot create line");
        lines.push(new_line);
    }

    add_test_train(&mut system, &lines, TRAIN_PER_LINE, TRAIN_CAPACITY).unwrap();
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
                let time = system.get_last_event_time();

                if time > last_printed_time + PRINT_INTERVAL {
                    last_printed_time = time;
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
                        let period = if time >= 0.0 {
                            ""
                        } else {
                            " WARMUP remaining "
                        };

                        println!(
                            "LOG {} {} -> {}",
                            period,
                            fmt_time(f64::abs(time)),
                            info.kind
                        );
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
