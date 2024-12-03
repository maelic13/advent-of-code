use std::fs::File;
use std::io::{BufRead, BufReader};

use simple_stopwatch::Stopwatch;

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let file = File::open("../inputs/2024/day1.txt").unwrap();
    let reader = BufReader::new(file);
    let mut firsts: Vec<isize> = vec![];
    let mut seconds: Vec<isize> = vec![];

    for line in reader.lines() {
        let line = line.unwrap();
        if line.is_empty() {
            continue;
        }
        let mut parts = line.split_whitespace();
        firsts.push(parts.next().unwrap().parse::<isize>().unwrap());
        seconds.push(parts.next().unwrap().parse::<isize>().unwrap());
    }
    let file_read_time = watch.us();

    // part 1
    firsts.sort();
    seconds.sort();
    let mut result: usize = 0;
    for (first, second) in firsts.iter().zip(seconds.iter()) {
        result += (first - second).abs() as usize;
    }

    println!("{}", result);
    let part1_time = watch.us() - file_read_time;

    // part 2
    let mut result: usize = 0;
    for first in firsts.iter() {
        result += *first as usize * seconds.iter().filter(|&&x| x == *first).count();
    }

    println!("{}", result);
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
