use std::error::Error;
use std::time::Instant;

use aoc_shared::{get_input, report_times};

fn main() -> Result<(), Box<dyn Error>> {
    let start = Instant::now();

    // read and parse file
    let input = get_input("2024", "1", true)?;

    for line in input {
        let line = line?;
        if line.is_empty() {
            continue;
        }
    }
    let file_read_time = start.elapsed();

    // part 1
    let result: isize = 0;
    println!("{}", result);
    let part1_time = start.elapsed();

    // part 2
    let result: isize = 0;
    println!("{}", result);
    let part2_time = start.elapsed();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
