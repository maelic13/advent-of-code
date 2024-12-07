use std::fs::File;
use std::io::{BufRead, BufReader};

use simple_stopwatch::Stopwatch;

fn count_valid(
    equations: &Vec<(usize, Vec<usize>)>,
    available_operands: Vec<fn(usize, usize) -> usize>,
) -> usize {
    let mut count: usize = 0;

    for (result, numbers) in equations {
        let (valid, result) = is_valid(
            numbers[0], result, &numbers[1..].to_vec(), &available_operands
        );
        if valid { count += result; }
    }
    count
}

fn is_valid(
    current_result: usize,
    expected_result: &usize,
    numbers: &Vec<usize>,
    available_operands: &Vec<fn(usize, usize) -> usize>,
) -> (bool, usize) {
    if numbers.is_empty() || current_result > *expected_result {
        return (current_result == *expected_result, current_result);
    }

    for operand in available_operands {
        let (valid, result) = is_valid(
            operand(current_result, numbers[0]),
            expected_result,
            &numbers[1..].to_vec(),
            available_operands
        );
        if valid { return (true, result); }
    }
    (false, 0)
}

fn add(item1: usize, item2: usize) -> usize { item1 + item2 }

fn mul(item1: usize, item2: usize) -> usize { item1 * item2 }

fn con(item1: usize, item2: usize) -> usize {
    (item1.to_string() + item2.to_string().as_str()).parse::<usize>().unwrap()
}

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let file = File::open("../inputs/2024/day7.txt").unwrap();
    let reader = BufReader::new(file);
    let mut equations: Vec<(usize, Vec<usize>)> = Vec::new();

    for line in reader.lines() {
        let line = line.unwrap();
        if line.is_empty() { continue; }

        let mut split = line.split(": ");
        equations.push(
            (split.next().unwrap().parse::<usize>().unwrap(),
             split.next().unwrap().split_whitespace().map(
                 |s| s.parse::<usize>().unwrap()
             ).collect())
        );
    }
    let file_read_time = watch.ms();

    // part 1
    println!("{}", count_valid(&equations, vec![add, mul]));
    let part1_time = watch.ms() - file_read_time;

    // part 2
    println!("{}", count_valid(&equations, vec![add, mul, con]));
    let part2_time = watch.ms() - part1_time - file_read_time;

    // report times
    println!();
    println!("Total time: {:.0} milliseconds.", watch.ms());
    println!("File read time: {:.1} milliseconds.", file_read_time);
    println!(
        "Execution time: {:.0} milliseconds.",
        part1_time + part2_time
    );
    println!();
    println!("Part 1 execution time: {:.0} milliseconds.", part1_time);
    println!("Part 2 execution time: {:.0} milliseconds.", part2_time);
}
