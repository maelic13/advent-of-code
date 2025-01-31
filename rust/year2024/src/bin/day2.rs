use std::time::Instant;

use aoc_shared::{read_input, report_times};

fn is_safe(report: &Vec<isize>) -> bool {
    let ascending = report
        .windows(2)
        .all(|w| w[1] - w[0] >= 1 && w[1] - w[0] <= 3);
    let descending = report
        .windows(2)
        .all(|w| w[0] - w[1] >= 1 && w[0] - w[1] <= 3);

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
    let start = Instant::now();

    // read and parse file
    let input = read_input("2024", "2", false).unwrap();
    let mut reports: Vec<Vec<isize>> = vec![];

    for line in input {
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
    let file_read_time = start.elapsed();

    // part 1
    println!(
        "{}",
        reports.iter().filter(|report| is_safe(&report)).count()
    );
    let part1_time = start.elapsed();

    // part 2
    println!(
        "{}",
        reports
            .iter()
            .filter(|report| is_safe_benevolent(&report))
            .count()
    );
    let part2_time = start.elapsed();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
