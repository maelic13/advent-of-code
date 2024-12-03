use std::fs::File;
use std::io::{BufRead, BufReader};

use simple_stopwatch::Stopwatch;

fn is_report_safe(report: &Vec<isize>, mut dampened: bool) -> bool {
    if report.len() < 2 { return true; }

    let mut report_to_check = report.clone();
    if report_to_check[1] < report_to_check[0] {
        report_to_check.reverse();
    }

    for i in 1..report_to_check.len() {
        let distance: isize = report_to_check[i] - report_to_check[i - 1];
        if 1 <= distance && distance <= 3 {
            continue;
        }

        if dampened { return false; }
        dampened = true
    }
    
    return true;
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
    let mut result: isize = 0;
    for report in &reports {
        if is_report_safe(report, true) {
            result += 1;
        }
    }

    println!("{}", result);
    let part1_time = watch.us() - file_read_time;

    // part 2
    let mut result: isize = 0;
    for report in &reports {
        if is_report_safe(report, false) {
            result += 1;
        }
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
