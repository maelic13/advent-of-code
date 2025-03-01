use std::time::Instant;

use aoc_shared::{read_input, report_times};

fn main() {
    let start = Instant::now();

    // read and parse file
    let input = read_input("2022", "1", false).unwrap();
    let mut sums: Vec<usize> = vec![];
    let mut buff: usize = 0;

    for line in input {
        let line = line.unwrap();
        if line.is_empty() {
            sums.push(buff);
            buff = 0;
            continue;
        }
        buff += line.parse::<usize>().unwrap();
    }
    let file_read_time = start.elapsed();

    // part 1
    println!("{}", sums.iter().max().unwrap());
    let part1_time = start.elapsed();

    // part 2
    sums.sort();
    println!("{}", sums[sums.len() - 3..].iter().sum::<usize>());
    let part2_time = start.elapsed();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
