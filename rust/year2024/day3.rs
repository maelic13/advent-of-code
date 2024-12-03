use std::fs::File;
use std::io::{BufRead, BufReader};

use regex::Regex;
use simple_stopwatch::Stopwatch;

fn section_analysis(section: &String) -> isize {
    let mut result: isize = 0;

    let re = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();
    for mul_args in re.captures_iter(section) {
        result += (&mul_args[1]).parse::<isize>().unwrap() * (&mul_args[2]).parse::<isize>().unwrap();
    }

    return result;
}

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let file = File::open("../inputs/2024/day3.txt").unwrap();
    let reader = BufReader::new(file);

    let memory_sections: Vec<String> = reader.lines().map(|l| l.unwrap()).collect();
    let file_read_time = watch.us();

    // part 1
    let mut result: isize = 0;
    for section in memory_sections {
        result += section_analysis(&section);
    }
    println!("{}", result);
    let part1_time = watch.us() - file_read_time;

    // part 2
    let mut result: usize = 0;
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
