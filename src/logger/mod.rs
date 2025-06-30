use std::fs::File;
use std::io::Write;

pub struct Logger {
    pub delay: File,
    pub people_in_stations: File,
}

impl Logger {
    pub fn new() -> Self {
        let mut new = Self {
            delay: File::create("output/delay.csv").expect("Cannot create log file"),
            people_in_stations: File::create("output/people.csv").expect("Cannot create log file"),
        };

        new.print_headers();
        new
    }

    fn print_headers(&mut self) {
        writeln!(self.delay, "Expected Time, Real Time, Line Name").expect("Cannot write to log");
        writeln!(self.people_in_stations, "Time, People, Station Name")
            .expect("Cannot write to log");
    }
}
