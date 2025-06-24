#![warn(clippy::pedantic)]
#![warn(clippy::nursery)]
#![warn(clippy::cargo)]
#![allow(clippy::cargo_common_metadata)]
#![allow(dead_code)]
#![allow(clippy::missing_const_for_fn)]

use crate::dataset::Dataset;
use crate::simulation::{Event, EventKind, Simulation};
use crate::train_lines::train_line::Direction;
use std::fs::File;

mod dataset;
mod graph;
mod simulation;
mod train_lines;

fn main() {
    let file = File::open("datasets/Wien.json").expect("Cannot open file");
    let dataset =
        serde_json::from_reader::<File, Dataset>(file).expect("JSON was not well-formatted");

    let mut system = Simulation::new(0, 1000, &dataset.stations);

    let mut lines = vec![];
    for data in &dataset.lines {
        let new_line = system.add_line(data);
        lines.push(new_line);
    }

    system.add_train(3, &lines[0], 2, Direction::Left).unwrap();
    system.add_train(5, &lines[1], 3, Direction::Right).unwrap();

    simulate(system);
}

fn simulate(mut system: Simulation) {
    let mut running = true;
    let mut i = 0;
    while running {
        println!("\nEVENT {i} {:?}:", system.peek_event());
        let current_event = system.peek_event().unwrap();
        print_dbg("BEFORE:", &system, &current_event);

        let result = system.simulation_step();

        match result {
            Ok(status) => running = !status,
            Err(error) => {
                println!("\n\nCORE DUMPED");
                println!("{:?}", system.trains);
                println!("\n\nSIMULATION ERRORED OUT");
                println!("{error}");
                running = false;
            }
        }

        print_dbg("AFTER:", &system, &current_event);
        i += 1;
    }
}

fn print_dbg(name: &str, system: &Simulation, current_event: &Event) {
    match current_event.kind {
        EventKind::Start | EventKind::End => {}
        EventKind::TrainArrive(train_id) => {
            print!("{name} ");

            let train = system
                .trains
                .get(&train_id)
                .expect("Arrival of a train that doesn't exist");

            let start = train.get_curr_station();
            let (end, dir) = train.get_next_station();
            println!(
                "{train_id} train {train:?} entering station {end} (from {start} with direction {dir:?}"
            );
        }
        EventKind::TrainDepart(train_id) => {
            print!("{name} ");

            let train = system
                .trains
                .get(&train_id)
                .expect("Departure of a train that doesn't exist");

            let start = train.get_curr_station();
            let (end, dir) = train.get_next_station();
            println!(
                "{train_id} train {train:?} exiting station {start} (to {end}) with direction {dir:?}"
            );
        }
        EventKind::PersonArrive(station_id) => {
            print!("{name} ");

            let station = system
                .graph
                .get_node(station_id)
                .expect("Person arrive to not existent station");

            println!("Person arrived ad station {station_id}: {station:?}");
        }
    }
}
