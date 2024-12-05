use std::fs::File;
use std::io::{BufRead, BufReader};

use regex::Regex;
use simple_stopwatch::Stopwatch;

fn count_words_in_string(string: &String, word: &str) -> usize {
    let mut words_counted: usize = 0;

    let re = Regex::new(word).unwrap();
    words_counted += re.captures_iter(&string).count();
    words_counted += re.captures_iter(&string.chars().rev().collect::<String>()).count();

    return words_counted;
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
            diagonal.push(word_search[j].chars().nth(word_search[0].len() - i - j - 1).unwrap());
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
            diagonal.push(word_search[j + i].chars().nth(word_search[0].len() - i - 1).unwrap());
        }
        words_counted += count_words_in_string(&diagonal, word);
    }

    return words_counted;
}

fn find_xmas(word_search: &Vec<String>) -> usize {
    let mut xmas_count: usize = 0;

    for i in 1..word_search.iter().count() - 1 {
        for j in 1..word_search[0].len() - 1 {
            if is_xmas(vec![&word_search[i - 1][j - 1..j + 2], &word_search[i][j - 1..j + 2], &word_search[i + 1][j - 1..j + 2]]) {
                xmas_count += 1;
            }
        }
    }

    return xmas_count;
}

fn is_xmas(area: Vec<&str>) -> bool {
    let first = String::from_iter(vec![area[0].chars().nth(0).unwrap(), area[1].chars().nth(1).unwrap(), area[2].chars().nth(2).unwrap()]);
    let second = String::from_iter(vec![area[2].chars().nth(0).unwrap(), area[1].chars().nth(1).unwrap(), area[0].chars().nth(2).unwrap()]);

    return (first == "MAS" || first == "SAM") && (second == "MAS" || second == "SAM");
}

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let file = File::open("../inputs/2024/day4.txt").unwrap();
    let reader = BufReader::new(file);
    let mut word_search: Vec<String> = vec!();

    for line in reader.lines() {
        let line = line.unwrap();
        if line.is_empty() { continue; }
        word_search.push(line);
    }
    let file_read_time = watch.us();

    // part 1
    println!("{}", count_words(&word_search, "XMAS"));
    let part1_time = watch.us() - file_read_time;

    // part 2
    println!("{}", find_xmas(&word_search));
    let part2_time = watch.us() - part1_time - file_read_time;

    // report times
    println!();
    println!("Total time: {:.0} milliseconds.", watch.ms());
    println!("File read time: {:.0} microseconds.", file_read_time);
    println!(
        "Execution time: {:.0} milliseconds.",
        (part1_time + part2_time) / 1_000.
    );
    println!();
    println!("Part 1 execution time: {:.0} milliseconds.", part1_time / 1_000.);
    println!("Part 2 execution time: {:.0} microseconds.", part2_time);
}
