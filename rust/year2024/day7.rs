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
            result, numbers, vec![], &available_operands
        );
        if valid {
            count += result;
        }
    }
    count
}

fn is_valid(
    expected_result: &usize, 
    numbers: &Vec<usize>, 
    mut operands: Vec<fn(usize, usize) -> usize>,
    available_operands: &Vec<fn(usize, usize) -> usize>,
) -> (bool, usize) {
    let mut result: usize = numbers[0];
    for (number, operand) in numbers[1..].iter().zip(operands.iter()) {
        result = operand(result, *number);
        if result > *expected_result { return (false, 0); }
    }

    if numbers.len() - 1 == operands.len() {
        return (result == *expected_result, result);
    }

    for available_operand in available_operands {
        operands.push(*available_operand);
        let (valid, result) = is_valid(
            expected_result, numbers, operands.clone(), available_operands
        );
        if valid { return (true, result); }
        operands.pop();
    }

    (false, 0)
}

fn add(item1: usize, item2: usize) -> usize {
    item1 + item2
}

fn mul(item1: usize, item2: usize) -> usize {
    item1 * item2
}

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
