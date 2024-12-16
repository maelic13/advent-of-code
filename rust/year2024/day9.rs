use std::fs::File;
use std::io::{BufRead, BufReader};

use simple_stopwatch::Stopwatch;

fn calculate_checksum(disk: &Vec<char>) -> usize {
    let mut checksum = 0;
    for (i, char) in disk.iter().enumerate() {
        if *char == '.' { continue; }
        checksum += i * char.to_digit(10).unwrap() as usize;
    }
    checksum
}

fn move_files_to_front(disk: &mut Vec<char>) {}

fn translate_disk_map(disk_map: &Vec<char>) -> Vec<char> {
    let mut disk = vec![];
    for (i, char) in disk_map.iter().enumerate() {
        let mut character = '.';
        if i % 2 == 0 {
            character = char::from_digit((i / 2) as u32, 10).unwrap();
        }
        for _ in 0..char.to_digit(10).unwrap() {
            disk.push(character);
        }
    }
    disk
}

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let file = File::open("../inputs/2024/day9_ex.txt").unwrap();
    let reader = BufReader::new(file);

    let mut disk_map: Vec<char> = vec![];
    for line in reader.lines() {
        let line = line.unwrap();
        if line.is_empty() { continue; }
        for char in line.chars() {
            disk_map.push(char);
        }
    }
    let file_read_time = watch.us();

    // part 1
    let mut disk = translate_disk_map(&disk_map);
    move_files_to_front(&mut disk);
    println!("{}", calculate_checksum(&disk));
    let part1_time = watch.us() - file_read_time;

    // part 2
    let result: isize = 0;
    println!("{}", result);
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
