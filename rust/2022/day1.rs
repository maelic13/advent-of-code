use std::fs::File;
use std::io::{BufRead, BufReader};

use simple_stopwatch::Stopwatch;

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let file = File::open("../inputs/2022/day1.txt").unwrap();
    let reader = BufReader::new(file);
    let mut sums: Vec<usize> = vec![];
    let mut buff: usize = 0;

    for line in reader.lines() {
        let line = line.unwrap();
        if line == "" {
            sums.push(buff);
            buff = 0;
            continue;
        }
        buff += line.parse::<usize>().unwrap();
    }
    let file_read_time = watch.us();

    // part 1
    println!("{}", sums.iter().max().unwrap());
    let part1_time = watch.us() - file_read_time;

    // part 2
    sums.sort();
    println!("{}", sums[sums.len() - 3..].iter().sum::<usize>());
    let part2_time = watch.us() - part1_time - file_read_time;

    // report times
    println!();
    println!("Total time: {:.0} microseconds.", watch.us());
    println!("File read time: {:.0} microseconds.", file_read_time);
    println!(
        "Execution time: {:.0} microseconds.",
        part1_time + part2_time
    );
    println!();
    println!("Part 1 execution time: {:.0} microseconds.", part1_time);
    println!("Part 2 execution time: {:.0} microseconds.", part2_time);
}
