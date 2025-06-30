#![allow(dead_code)]
use crate::train_lines::Time;

pub const fn from_hour(hour: f64) -> Time {
    hour
}

pub const fn from_minutes(minutes: f64) -> Time {
    minutes / 60.0
}

pub const fn from_seconds(seconds: f64) -> Time {
    seconds / 3600.0
}

pub fn fmt_time(time: Time) -> String {
    let hours = time.trunc();

    let minutes_with_dot = (time - hours) * 60.0;
    let minutes = minutes_with_dot.trunc();
    let seconds = minutes_with_dot - minutes;

    format!("{hours:02.0}:{minutes:02.0}:{seconds:02.0}")
}
