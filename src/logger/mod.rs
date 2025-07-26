use crate::train_lines::Time;
use std::fs;
use std::fs::File;
use std::io::{BufWriter, Write};

pub struct Logger {
    delay: BufWriter<File>,
    people_in_stations: BufWriter<File>,
    time_to_board: BufWriter<File>,
    people_served: BufWriter<File>,
}

impl Logger {
    pub fn new() -> Self {
        if !fs::exists("output").expect("Cannot check state") {
            fs::create_dir("output").expect("Could not create output/ directory");
        }

        let mut new = Self {
            delay: BufWriter::new(
                File::create("output/delay.csv")
                    .expect("Cannot create log file, probably need to create output directory"),
            ),
            people_in_stations: BufWriter::new(
                File::create("output/people.csv").expect("Cannot create log file"),
            ),
            time_to_board: BufWriter::new(
                File::create("output/board_time.csv").expect("Cannot create log file"),
            ),
            people_served: BufWriter::new(
                File::create("output/people_served.csv").expect("Cannot create log file"),
            ),
        };

        new.print_headers();
        new
    }

    pub fn flush(&mut self) {
        self.time_to_board
            .flush()
            .expect("Could not flush log file");
        self.people_in_stations
            .flush()
            .expect("Could not flush log file");
        self.people_served
            .flush()
            .expect("Could not flush log file");
        self.delay.flush().expect("Could not flush log file");
    }

    fn print_headers(&mut self) {
        self.println_delay(
            0.0,
            "Expected Time (Seconds), Real Time (Seconds), Line Name",
        );
        self.println_people_in_station(0.0, "Time, People, Station Name");
        self.println_time_to_board(
            0.0,
            "Time (h), StationId, Line Name, Time To Board (min), People Boarded",
        );
        self.println_people_served(0.0, "Time, People Served Since Last Interval");
    }

    fn println_to_file(file: &mut BufWriter<File>, str: &str) {
        writeln!(file, "{str}").expect("Cannot write to log");
    }

    pub fn println_delay(&mut self, time: Time, str: &str) {
        if time >= 0.0 {
            Self::println_to_file(&mut self.delay, str);
        }
    }

    pub fn println_people_in_station(&mut self, time: Time, str: &str) {
        if time >= 0.0 {
            Self::println_to_file(&mut self.people_in_stations, str);
        }
    }

    pub fn println_people_served(&mut self, time: Time, str: &str) {
        if time >= 0.0 {
            Self::println_to_file(&mut self.people_served, str);
        }
    }

    pub fn println_time_to_board(&mut self, time: Time, str: &str) {
        if time >= 0.0 {
            Self::println_to_file(&mut self.time_to_board, str);
        }
    }
}
