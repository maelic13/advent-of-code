use std::fs::File;
use std::io::{BufReader, BufRead};

use simple_stopwatch::Stopwatch;


fn main() {
    let watch = Stopwatch::start_new();

    let file = File::open("../inputs/2022/day1.txt").unwrap();
    let reader = BufReader::new(file);
    let mut sums: Vec<usize> = vec![];
    let mut buff: usize = 0;

    for line in reader.lines() {
        let line = line.unwrap();
        if line == "" {
            sums.push(buff);
            buff = 0;
            continue;
        }
        buff += line.parse::<usize>().unwrap();
    }

    // part 1
    println!("{}", sums.iter().max().unwrap());

    // part 2
    sums.sort();
    println!("{}", sums[sums.len() - 3..].iter().sum::<usize>());

    println!("Execution time: {:.0} microseconds.", watch.us());
}
