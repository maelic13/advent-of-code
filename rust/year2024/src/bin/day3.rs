use aoc_shared::{get_input, report_times};
use regex::Regex;
use simple_stopwatch::Stopwatch;

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
    let watch = Stopwatch::start_new();

    // read and parse file
    let input = get_input("2024", "3", false).unwrap();

    let memory_sections: String = input.map(|l| l.unwrap()).collect::<Vec<_>>().join("");
    let file_read_time = watch.us();

    // part 1
    println!("{}", section_analysis(&memory_sections));
    let part1_time = watch.us();

    // part 2
    println!("{}", advanced_section_analysis(&memory_sections));
    let part2_time = watch.us();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
