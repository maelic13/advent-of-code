use std::time::Instant;

use regex::Regex;

use aoc_shared::{read_input, report_times};

fn count_words_in_string(string: &String, word: &str) -> usize {
    let mut words_counted: usize = 0;

    let re = Regex::new(word).unwrap();
    words_counted += re.captures_iter(&string).count();
    words_counted += re
        .captures_iter(&string.chars().rev().collect::<String>())
        .count();

    words_counted
}

fn count_words(word_search: &Vec<String>, word: &str) -> usize {
    let mut words_counted: usize = 0;

    // search lines
    for line in word_search {
        words_counted += count_words_in_string(line, word);
    }

    // search columns
    for i in 0..word_search[0].len() {
        let mut column: String = String::from("");
        for j in 0..word_search.iter().count() {
            column.push(word_search[j].chars().nth(i).unwrap());
        }
        words_counted += count_words_in_string(&column, word);
    }

    // search diagonals from top
    for i in 0..word_search[0].len() {
        let mut diagonal = String::from("");
        for j in 0..word_search.iter().count() - i {
            diagonal.push(word_search[j].chars().nth(i + j).unwrap());
        }
        words_counted += count_words_in_string(&diagonal, word);

        let mut diagonal = String::from("");
        for j in 0..word_search.iter().count() - i {
            diagonal.push(
                word_search[j]
                    .chars()
                    .nth(word_search[0].len() - i - j - 1)
                    .unwrap(),
            );
        }
        words_counted += count_words_in_string(&diagonal, word);
    }

    // diagonals from side
    for j in 1..word_search.iter().count() {
        let mut diagonal = String::from("");
        for i in 0..word_search.iter().count() - j {
            diagonal.push(word_search[j + i].chars().nth(i).unwrap());
        }
        words_counted += count_words_in_string(&diagonal, word);

        let mut diagonal = String::from("");
        for i in 0..word_search.iter().count() - j {
            diagonal.push(
                word_search[j + i]
                    .chars()
                    .nth(word_search[0].len() - i - 1)
                    .unwrap(),
            );
        }
        words_counted += count_words_in_string(&diagonal, word);
    }

    words_counted
}

fn find_xmas(word_search: &Vec<String>) -> usize {
    let mut xmas_count: usize = 0;

    for i in 1..word_search.iter().count() - 1 {
        for j in 1..word_search[0].len() - 1 {
            if is_xmas(vec![
                &word_search[i - 1][j - 1..j + 2],
                &word_search[i][j - 1..j + 2],
                &word_search[i + 1][j - 1..j + 2],
            ]) {
                xmas_count += 1;
            }
        }
    }

    xmas_count
}

fn is_xmas(area: Vec<&str>) -> bool {
    let first = String::from_iter(vec![
        area[0].chars().nth(0).unwrap(),
        area[1].chars().nth(1).unwrap(),
        area[2].chars().nth(2).unwrap(),
    ]);
    let second = String::from_iter(vec![
        area[2].chars().nth(0).unwrap(),
        area[1].chars().nth(1).unwrap(),
        area[0].chars().nth(2).unwrap(),
    ]);

    (first == "MAS" || first == "SAM") && (second == "MAS" || second == "SAM")
}

fn main() {
    let start = Instant::now();

    // read and parse file
    let input = read_input("2024", "4", false).unwrap();
    let mut word_search: Vec<String> = vec![];

    for line in input {
        let line = line.unwrap();
        if line.is_empty() {
            continue;
        }
        word_search.push(line);
    }
    let file_read_time = start.elapsed();

    // part 1
    println!("{}", count_words(&word_search, "XMAS"));
    let part1_time = start.elapsed();

    // part 2
    println!("{}", find_xmas(&word_search));
    let part2_time = start.elapsed();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
