use aoc_shared::{get_input, report_times};
use simple_stopwatch::Stopwatch;

fn count_stones_after_blinks(stones: &Vec<String>, blinks: usize) -> usize {
    let mut to_calculate: Vec<(String, usize)> = stones
        .iter()
        .map(|s| (s.clone(), 0))
        .collect();
    let mut count: usize = 0;

    while !to_calculate.is_empty() {
        let (stone, blink_num) = to_calculate.pop().unwrap();
        if blink_num == blinks {
            count += 1;
            continue;
        }

        match blink(&stone) {
            (new_stone_1, Some(new_stone_2)) => {
                to_calculate.push((new_stone_1, blink_num + 1));
                to_calculate.push((new_stone_2, blink_num + 1));
            }
            (new_stone_1, None) => {
                to_calculate.push((new_stone_1, blink_num + 1));
            }
        }
    }

    count
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
            .trim_start_matches('0').to_string();
        if second_half.is_empty() {
            // optimization - insert result of rule 1
            second_half = "1".to_string();
        }
        return (first_half, Some(second_half));

    }

    // rule 3
    ((stone.parse::<usize>().unwrap() * 2024).to_string(), None)
}

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let input = get_input("2024", "11", false).unwrap();
    let mut stones: Vec<String> = vec![];
    let file_read_time = watch.us();

    for line in input {
        let line = line.unwrap();
        if line.is_empty() { continue; }
        for c in line.split_whitespace() {
            stones.push(c.to_string());
        }
    }

    // part 1
    println!("{}", count_stones_after_blinks(&stones, 25));
    let part1_time = watch.us();

    // part 2
    // println!("{}", count_stones_after_blinks(&stones, 75));
    let part2_time = watch.us();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
