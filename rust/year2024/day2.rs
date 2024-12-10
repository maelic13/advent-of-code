use std::fs::File;
use std::io::{BufRead, BufReader};

use simple_stopwatch::Stopwatch;

fn is_safe(report: &Vec<isize>) -> bool {
    let ascending = report.windows(2).all(|w| w[1] - w[0] >= 1 && w[1] - w[0] <= 3);
    let descending = report.windows(2).all(|w| w[0] - w[1] >= 1 && w[0] - w[1] <= 3);

    ascending || descending
}

fn is_safe_benevolent(report: &Vec<isize>) -> bool {
    (0..report.len()).any(|i| {
        let mut reduced = report.clone();
        reduced.remove(i);
        is_safe(&reduced)
    })
}

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let file = File::open("../inputs/2024/day2.txt").unwrap();
    let reader = BufReader::new(file);
    let mut reports: Vec<Vec<isize>> = vec![];

    for line in reader.lines() {
        let line = line.unwrap();
        if line.is_empty() {
            continue;
        }
        let mut report: Vec<isize> = vec![];
        for number in line.split_whitespace() {
            report.push(number.parse().unwrap());
        }
        reports.push(report);
    }
    let file_read_time = watch.us();

    // part 1
    println!("{}", reports.iter().filter(|report| is_safe(&report)).count());
    let part1_time = watch.us() - file_read_time;

    // part 2
    println!("{}", reports.iter().filter(|report| is_safe_benevolent(&report)).count());
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
