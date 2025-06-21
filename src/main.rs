#![warn(clippy::pedantic)]
#![warn(clippy::nursery)]
#![warn(clippy::cargo)]
#![allow(clippy::cargo_common_metadata)]
#![allow(dead_code)]
#![allow(clippy::missing_const_for_fn)]

use crate::simulation::{Event, EventKind, Simulation};
use crate::train_lines::train_line::{Direction, TrainLine};

mod graph;
mod simulation;
mod train_lines;

fn main() {
    // let file = File::open("datasets/London.json").expect("Cannot open file");
    // let json: serde_json::Value =
    //     serde_json::from_reader(file).expect("JSON was not well-formatted");
    //
    // println!("{json}");

    let mut system = Simulation::new(0, 1000);
    let line = TrainLine::new(vec![1, 2, 3, 4, 5]);
    let line = system.add_line(line);
    system.add_train(3, &line, 2, Direction::Left).unwrap();
    system.add_train(5, &line, 3, Direction::Right).unwrap();

    simulate(system);
}

fn simulate(mut system: Simulation) {
    let mut running = true;
    let mut i = 0;
    while running {
        println!("\nEVENT {i} {:?}:", system.peek_event());
        let current_event = system.peek_event().unwrap();
        print!("BEFORE:");
        print_dbg(&system, &current_event);

        match system.simulation_step() {
            Ok(status) => running = !status,
            Err(error) => {
                println!("Simulation errored out");
                println!("{error}");
                println!();
                println!("{system:?}");
                running = false;
            }
        }

        i += 1;

        print!("BEFORE:");
        print_dbg(&system, &current_event);
    }
}

fn print_dbg(system: &Simulation, current_event: &Event) {
    match current_event.kind {
        EventKind::Start | EventKind::End => {}
        EventKind::TrainArrive(train_id) => {
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
            let station = system
                .graph
                .get_node(station_id)
                .expect("Person arrive to not existent station");

            println!("Person arrived ad station {station_id}: {station:?}");
        }
    }
}
