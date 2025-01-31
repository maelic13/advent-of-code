use std::collections::HashMap;
use std::time::Instant;

use aoc_shared::{read_input, report_times};

fn main() {
    let start = Instant::now();

    // read and parse file
    let input = read_input("2024", "1", false).unwrap();
    let mut firsts: Vec<usize> = vec![];
    let mut seconds: Vec<usize> = vec![];

    for line in input {
        let line = line.unwrap();
        if line.is_empty() {
            continue;
        }
        let mut parts = line.split_whitespace();
        firsts.push(parts.next().unwrap().parse::<usize>().unwrap());
        seconds.push(parts.next().unwrap().parse::<usize>().unwrap());
    }
    let file_read_time = start.elapsed();

    // part 1
    firsts.sort();
    seconds.sort();
    let mut result: usize = 0;
    for (first, second) in firsts.iter().zip(seconds.iter()) {
        result += first.abs_diff(*second);
    }

    println!("{}", result);
    let part1_time = start.elapsed();

    // part 2
    let mut hash_map: HashMap<usize, usize> = HashMap::new();
    for second in seconds {
        hash_map.insert(
            second,
            match hash_map.get(&second) {
                Some(i) => i + 1,
                None => 1,
            },
        );
    }

    result = firsts
        .iter()
        .map(|&i| i * hash_map.get(&i).unwrap_or_else(|| &0))
        .sum();
    println!("{}", result);
    let part2_time = start.elapsed();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
