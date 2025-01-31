use std::time::Instant;

use regex::Regex;

use aoc_shared::{read_input, report_times};

fn advanced_section_analysis(section: &String) -> usize {
    let mut result: usize = 0;

    for part in section.split("do()") {
        result += section_analysis(
            &part
                .split("don't()")
                .next()
                .unwrap()
                .parse::<String>()
                .unwrap(),
        );
    }

    result
}

fn section_analysis(section: &String) -> usize {
    let mut result: usize = 0;

    let re = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();
    for mul_args in re.captures_iter(section) {
        result += &mul_args[1].parse::<usize>().unwrap() * &mul_args[2].parse::<usize>().unwrap();
    }

    result
}

fn main() {
    let start = Instant::now();

    // read and parse file
    let input = read_input("2024", "3", false).unwrap();

    let memory_sections: String = input.map(|l| l.unwrap()).collect::<Vec<_>>().join("");
    let file_read_time = start.elapsed();

    // part 1
    println!("{}", section_analysis(&memory_sections));
    let part1_time = start.elapsed();

    // part 2
    println!("{}", advanced_section_analysis(&memory_sections));
    let part2_time = start.elapsed();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
