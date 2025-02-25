use std::time::Instant;

use aoc_shared::{read_input, report_times};

fn count_valid(
    equations: &Vec<(usize, Vec<usize>)>,
    available_operands: &[fn(usize, usize) -> usize],
) -> usize {
    let mut count: usize = 0;

    for (result, numbers) in equations {
        match is_valid(1, numbers[0], *result, numbers, available_operands) {
            (true, res) => count += res,
            _ => continue,
        }
    }
    count
}

fn is_valid(
    current_index: usize,
    current_result: usize,
    expected_result: usize,
    numbers: &Vec<usize>,
    available_operands: &[fn(usize, usize) -> usize],
) -> (bool, usize) {
    if current_index == numbers.len() || current_result > expected_result {
        return (current_result == expected_result, current_result);
    }

    for operand in available_operands {
        match is_valid(
            current_index + 1,
            operand(current_result, numbers[current_index]),
            expected_result,
            numbers,
            available_operands,
        ) {
            (true, res) => return (true, res),
            _ => continue,
        }
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
    // Instead of transfer to String and concatenate, multiply item1 by 10 to the power of item2's
    // number of digits and add item2. This is much faster.
    item1 * 10usize.pow(item2.ilog10() + 1) + item2
}

fn main() {
    let start = Instant::now();

    // read and parse file
    let input = read_input("2024", "7", false).unwrap();
    let mut equations: Vec<(usize, Vec<usize>)> = Vec::new();

    for line in input {
        let line = line.unwrap();
        if line.is_empty() {
            continue;
        }

        let mut split = line.split(": ");
        equations.push((
            split.next().unwrap().parse::<usize>().unwrap(),
            split
                .next()
                .unwrap()
                .split_whitespace()
                .map(|s| s.parse::<usize>().unwrap())
                .collect(),
        ));
    }
    let file_read_time = start.elapsed();

    // part 1
    let part1_result = count_valid(&equations, &[mul, add]);
    let part1_time = start.elapsed();

    // part 2
    let part2_result = count_valid(&equations, &[mul, add, con]);
    let part2_time = start.elapsed();

    // report results and times
    println!("{part1_result}");
    println!("{part2_result}");
    report_times(file_read_time, part1_time, part2_time);
}
