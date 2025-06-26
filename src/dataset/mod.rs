use crate::train_lines::StationId;
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize, Debug)]
pub struct Dataset {
    pub stations: Vec<StationData>,
    pub lines: Vec<LineData>,
}

#[derive(Deserialize, Serialize, Debug)]
pub struct LineData {
    pub name: String,
    pub color: String,
    pub stops: Vec<StationId>,
}
#[derive(Deserialize, Serialize, Debug)]
pub struct StationData {
    pub lat: f64,
    pub lon: f64,
    pub name: String,
}
