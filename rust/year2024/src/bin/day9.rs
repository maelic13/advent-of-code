use std::iter::zip;
use std::time::Instant;

use aoc_shared::{read_input, report_times};

fn calculate_checksum(disk: &Vec<String>) -> usize {
    let mut checksum = 0;
    for (i, char) in disk.iter().enumerate() {
        if char == "." {
            continue;
        }
        checksum += i * char.parse::<usize>().unwrap();
    }
    checksum
}

fn move_bits_to_front(disk: &mut Vec<String>) {
    let disk_len: usize = disk.len();
    let disk_last_index: usize = disk_len - 1;

    for i in 0..disk_len {
        if disk[i] != "." {
            continue;
        }
        for j in 0..disk_len {
            if disk_last_index - j <= i {
                break;
            }
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
    let mut ignore_files: Vec<String> = vec![];

    for i in 0..disk_len {
        let file_identifier = disk[disk_last_index - i].to_string();
        if file_identifier == "." || ignore_files.contains(&file_identifier) {
            continue;
        }

        // locate full file
        let mut file_start_index: usize = 0;
        let file_end_index: usize = disk_last_index - i;
        for j in 1..(disk_len - i) {
            if disk[file_end_index - j] == file_identifier {
                continue;
            }
            file_start_index = file_end_index - j + 1;
            break;
        }
        ignore_files.push(file_identifier);

        // find large enough space if exists
        let mut space_start_index: usize = 1;
        let mut space_end_index: usize = 0;
        for j in 0..file_start_index {
            if disk[j] != "." {
                continue;
            }
            if j >= file_start_index {
                space_end_index = disk_len;
                break;
            }

            space_start_index = j;
            for k in 0..(file_end_index - file_start_index + 2) {
                if disk[j + k] != "." {
                    break;
                }
                space_end_index = j + k;
            }

            if (space_end_index - space_start_index) >= (file_end_index - file_start_index) {
                break;
            }
        }

        if (space_end_index - space_start_index) < (file_end_index - file_start_index) {
            continue;
        }

        if space_end_index >= file_start_index {
            break;
        }

        // move file
        for (space_index, file_index) in zip(
            space_start_index..space_end_index + 1,
            file_start_index..file_end_index + 1,
        ) {
            disk.swap(file_index, space_index);
        }
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

#[allow(dead_code)]
fn print_disk(disk: &Vec<String>) {
    for char in disk {
        print!("{} ", char);
    }
    println!();
}

fn main() {
    let start = Instant::now();

    // read and parse file
    let input = read_input("2024", "9", false).unwrap();
    let mut disk_map: Vec<char> = vec![];

    for line in input {
        let line = line.unwrap();
        if line.is_empty() {
            continue;
        }
        for char in line.chars() {
            disk_map.push(char);
        }
    }
    let mut disk: Vec<String> = translate_disk_map(&disk_map);
    let file_read_time = start.elapsed();

    // part 1
    let mut modified_disk = disk.to_vec();
    move_bits_to_front(&mut modified_disk);
    println!("{}", calculate_checksum(&modified_disk));
    let part1_time = start.elapsed();

    // part 2
    move_files_to_front(&mut disk);
    println!("{}", calculate_checksum(&disk));
    let part2_time = start.elapsed();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
