use aoc_shared::{get_input, report_times};
use simple_stopwatch::Stopwatch;

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let input = get_input("2024", "1", true).unwrap();

    for line in input {
        let line = line.unwrap();
        if line.is_empty() { continue; }
    }
    let file_read_time = watch.us();

    // part 1
    let result: isize = 0;
    println!("{}", result);
    let part1_time = watch.us();

    // part 2
    let result: isize = 0;
    println!("{}", result);
    let part2_time = watch.us();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
