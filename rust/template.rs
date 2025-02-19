use std::error::Error;
use std::time::Instant;

use aoc_shared::{read_input, report_times};

fn main() -> Result<(), Box<dyn Error>> {
    let start = Instant::now();

    // read and parse file
    let input = read_input("2024", "1", true)?;

    for line in input {
        let line = line?;
        if line.is_empty() {
            continue;
        }
    }
    let file_read_time = start.elapsed();

    // part 1
    let part1_result: isize = 0;
    let part1_time = start.elapsed();

    // part 2
    let part2_result: isize = 0;
    let part2_time = start.elapsed();

    // report results and times
    println!("{part1_result}");
    println!("{part2_result}");
    report_times(file_read_time, part1_time, part2_time);
    Ok(())
}
