use std::fs;
use std::fs::File;
use std::io::Write;

pub struct Logger {
    pub delay: File,
    pub people_in_stations: File,
    pub time_to_board: File,
}

impl Logger {
    pub fn new() -> Self {
        if !fs::exists("output").expect("Cannot check state") {
            fs::create_dir("output").expect("Could not create output/ directory");
        }

        let mut new = Self {
            delay: File::create("output/delay.csv")
                .expect("Cannot create log file, probably need to create output directory"),
            people_in_stations: File::create("output/people.csv").expect("Cannot create log file"),
            time_to_board: File::create("output/board_time.csv").expect("Cannot create log file"),
        };

        new.print_headers();
        new
    }

    fn print_headers(&mut self) {
        writeln!(self.delay, "Expected Time, Real Time, Line Name").expect("Cannot write to log");
        writeln!(self.people_in_stations, "Time, People, Station Name")
            .expect("Cannot write to log");
        writeln!(
            self.time_to_board,
            "Time, StationId, Line Name, Time To Board"
        )
        .expect("Cannot write to log");
    }
}
