use crate::train_lines::Time;
use crate::utils::time::{from_days, from_hour, from_minutes, from_seconds};

// Simulation lenght
pub const WARMUP_TIME: Time = from_days(30.0);
pub const SIM_LEN: Time = from_days(30.0);
pub const PRINT_INTERVAL: Time = from_hour(6.0);

// Crash related
pub const TIME_TO_RECOVER: Time = from_minutes(20.0);
pub const TIME_AT_STATION: Time = from_seconds(20.0);
pub const KM_BEFORE_CRASHING: f64 = 10_000.0;

// Speed
pub const AVG_SPEED_M_S: f64 = 32.5 / 3.6;
pub const VAR_SPEED: f64 = 20.0;
pub const MAX_SPEED_M_S: f64 = 80.0 / 3.6;
pub const MIN_SPEED_M_S: f64 = 5.0 / 3.6;

// Capacity & arrival rate
pub const TRAIN_CAPACITY: usize = 800;
pub const TRAIN_PER_LINE: usize = 10;
pub const EDGE_MAX_CAPACITY: usize = 1;
pub const AVERAGE_PEOPLE_ARRIVE_TIME: Time = from_seconds(10.0);

// Just for performance and data sampling time tradeoff
pub const SNAPSHOT_TIME_PEOPLE_IN_STATION: Time = from_minutes(5.0);
pub const SNAPSHOT_TIME_PEOPLE_SERVED: Time = from_minutes(10.0);
