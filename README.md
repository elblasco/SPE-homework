# Simulation and Performance Evaluation

## Final Project

Simulation and evalutaion of Vienna metro system.

### Run it

In to order to get the best performances compile it with the release flag

```bash
cargo run -r
```

For debug purposes only, use the following command that log each and every event

```bash
cargo run 
```

In order to run the data anlysis scripts use,

```bash
cd data-analysis
./run-all.sh
```

The graphs will be produced as `.svg` files under `./data-analysis/img/`

### Tune it

If you want to change the simulation paramters modify the values in `./src/utils/config.rs`

### Report

https://www.overleaf.com/read/mcwztnrtjhdg#06dc9d

## Assignements

Are in the `assignments` directory.
