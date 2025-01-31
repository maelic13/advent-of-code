use std::collections::HashMap;
use std::time::Instant;

use aoc_shared::{read_input, report_times};

fn count_stones_after_blinks(mut stones: HashMap<String, usize>, blinks: usize) -> usize {
    for _ in 0..blinks {
        let mut new_stones: HashMap<String, usize> = HashMap::new();

        for (stone, quantity) in &stones {
            match blink(&stone) {
                (new_stone_1, Some(new_stone_2)) => {
                    *new_stones.entry(new_stone_1.to_string()).or_insert(0) += quantity;
                    *new_stones.entry(new_stone_2.to_string()).or_insert(0) += quantity;
                }
                (new_stone_1, None) => {
                    *new_stones.entry(new_stone_1.to_string()).or_insert(0) += quantity;
                }
            }
        }
        stones = new_stones;
    }

    stones.values().sum()
}

fn blink(stone: &String) -> (String, Option<String>) {
    // rule 1
    if stone == "0" {
        return ("1".to_string(), None);
    }

    // rule 2
    let stone_len: usize = stone.len();
    if stone_len % 2 == 0 {
        let first_half = stone[0..stone_len / 2].to_string();
        let mut second_half = stone[stone_len / 2..stone_len]
            .trim_start_matches('0')
            .to_string();
        if second_half.is_empty() {
            second_half = "0".to_string();
        }
        return (first_half, Some(second_half));
    }

    // rule 3
    ((stone.parse::<usize>().unwrap() * 2024).to_string(), None)
}

fn main() {
    let start = Instant::now();

    // read and parse file
    let input = read_input("2024", "11", false).unwrap();
    let mut stones: HashMap<String, usize> = HashMap::new();
    let file_read_time = start.elapsed();

    for line in input {
        let line = line.unwrap();
        if line.is_empty() {
            continue;
        }
        for c in line.split_whitespace() {
            *stones.entry(c.to_string()).or_insert(0) += 1;
        }
    }

    // part 1
    println!("{}", count_stones_after_blinks(stones.clone(), 25));
    let part1_time = start.elapsed();

    // part 2
    println!("{}", count_stones_after_blinks(stones, 75));
    let part2_time = start.elapsed();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
