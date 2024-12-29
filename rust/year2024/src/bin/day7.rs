use aoc_shared::{get_input, report_times};
use simple_stopwatch::Stopwatch;

fn count_valid(
    equations: &Vec<(usize, Vec<usize>)>,
    available_operands: Vec<fn(usize, usize) -> usize>,
) -> usize {
    let mut count: usize = 0;

    for (result, numbers) in equations {
        let (valid, result) = is_valid(
            numbers[0],
            result,
            &numbers[1..].to_vec(),
            &available_operands,
        );
        if valid {
            count += result;
        }
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
            available_operands,
        );
        if valid {
            return (true, result);
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
    (item1.to_string() + item2.to_string().as_str())
        .parse::<usize>()
        .unwrap()
}

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let input = get_input("2024", "7", false).unwrap();
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
    let file_read_time = watch.us();

    // part 1
    println!("{}", count_valid(&equations, vec![add, mul]));
    let part1_time = watch.us();

    // part 2
    println!("{}", count_valid(&equations, vec![add, mul, con]));
    let part2_time = watch.us();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
