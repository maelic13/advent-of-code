use std::fs::File;
use std::io::{BufRead, BufReader};

use regex::Regex;
use simple_stopwatch::Stopwatch;

fn advanced_section_analysis(section: &String) -> usize {
    let mut result: usize = 0;

    for part in section.split("do()") {
        result += section_analysis(
            &part.split("don't()").next().unwrap().parse::<String>().unwrap()
        );
    }

    return result;
}

fn section_analysis(section: &String) -> usize {
    let mut result: usize = 0;

    let re = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();
    for mul_args in re.captures_iter(section) {
        result += &mul_args[1].parse::<usize>().unwrap() * &mul_args[2].parse::<usize>().unwrap();
    }

    return result;
}

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let file = File::open("../inputs/2024/day3.txt").unwrap();
    let reader = BufReader::new(file);

    let memory_sections: String =
        reader.lines()
            .map(|l| l.unwrap())
            .collect::<Vec<_>>().join("");
    let file_read_time = watch.us();

    // part 1
    println!("{}", section_analysis(&memory_sections));
    let part1_time = watch.us() - file_read_time;

    // part 2
    println!("{}", advanced_section_analysis(&memory_sections));
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
