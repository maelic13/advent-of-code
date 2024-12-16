use std::fs::File;
use std::io::{BufRead, BufReader};

use simple_stopwatch::Stopwatch;

fn calculate_checksum(disk: &Vec<String>) -> usize {
    let mut checksum = 0;
    for (i, char) in disk.iter().enumerate() {
        if char == "." { continue; }
        checksum += i * char.parse::<usize>().unwrap();
    }
    checksum
}

fn move_bits_to_front(disk: &mut Vec<String>) {
    let disk_len: usize = disk.len();
    let disk_last_index: usize = disk_len - 1;

    for i in 0..disk_len {
        if disk[i] != "." { continue; }
        for j in 0..disk_len {
            if disk_last_index - j <= i { break; }
            if disk[disk_last_index - j] != "." {
                disk.swap(i, disk_last_index - j);
                break;
            }
        }
    }
}

fn move_files_to_front(disk: &mut Vec<String>) {
    let disk_len: usize = disk.len();
    let disk_last_index: usize = disk_len - 1;
    let mut last_checked_index: usize = disk_last_index;

    for i in 0..disk_last_index {
        if disk[i] != "." { continue; }

        let mut empty_space_size = 0;
        for j in 1..disk_last_index {
            if disk[i + j] != "." {
                empty_space_size += j;
                break;
            }
        }

        let mut current_file: String = String::from("0");
        for j in 0..last_checked_index {
            if last_checked_index - j <= i { break; }

            let char: String = disk[last_checked_index - j].to_string();
            if char == current_file || char == "." { continue; };
            current_file = char;

            let mut file_size: usize = 0;
            for k in 1..disk_len {
                if disk[last_checked_index - j - k] != current_file {
                    file_size += k;
                    break;
                }
            }
            if file_size > empty_space_size { continue; }
            for k in 0..file_size {
                println!("Moving {} to {}", i + k, disk_len - j - file_size + k);
                disk.swap(i + k, disk_len - j - file_size + k);
            }
            last_checked_index = last_checked_index - j - file_size;
            break;
        }
        print_disk(&disk);
    }
}

fn move_files_to_front2(disk: &mut Vec<String>) {
    let disk_len: usize = disk.len();
    let disk_last_index: usize = disk_len - 1;
    let mut current_file: String;

    for i in 0..disk_len {
        let char = disk[disk_last_index - i].to_string();
        if char == "." { continue; }

        current_file = char;
        let mut file_size: usize = 0;
        for j in 0..disk_last_index {
            if disk[disk_last_index - i - j] != current_file {
                file_size += j;
                break;
            }
        }

        for j in 0..disk_len - file_size {
            if j > i { break; }
            if disk[j] != "." { continue; }
            let mut empty_space_size: usize = 0;
            for k in 0..file_size {
                if disk[j + k] != "." { break; }
                empty_space_size = k + 1;
            }
            println!("Empty size: {}, file size: {}", empty_space_size, file_size);
            if empty_space_size < file_size{ continue; }

            for k in 0..file_size {
                disk.swap(j + k, disk_len - i - file_size + k);
            }
            break;
        }

        print_disk(&disk);
    }
}

fn translate_disk_map(disk_map: &Vec<char>) -> Vec<String> {
    let mut disk: Vec<String> = vec![];
    for (i, char) in disk_map.iter().enumerate() {
        let mut character = ".".to_string();
        if i % 2 == 0 {
            character = (i / 2).to_string();
        }
        for _ in 0..char.to_digit(10).unwrap() {
            disk.push(character.clone());
        }
    }
    disk
}

fn print_disk(disk: &Vec<String>) {
    for char in disk {
        print!("{}", char);
    }
    println!();
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

    let mut disk: Vec<String> = translate_disk_map(&disk_map);

    // part 1
    let mut modified_disk = disk.to_vec();
    move_bits_to_front(&mut modified_disk);
    println!("{}", calculate_checksum(&modified_disk));
    let part1_time = watch.us() - file_read_time;

    // part 2
    print_disk(&disk);
    move_files_to_front2(&mut disk);
    print_disk(&disk);
    println!("{}", calculate_checksum(&disk));
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
