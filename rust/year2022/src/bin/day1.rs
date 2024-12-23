use aoc_shared::{get_input, report_times};
use simple_stopwatch::Stopwatch;

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let input = get_input("2022", "1", false).unwrap();
    let mut sums: Vec<usize> = vec![];
    let mut buff: usize = 0;

    for line in input {
        let line = line.unwrap();
        if line.is_empty() {
            sums.push(buff);
            buff = 0;
            continue;
        }
        buff += line.parse::<usize>().unwrap();
    }
    let file_read_time = watch.us();

    // part 1
    println!("{}", sums.iter().max().unwrap());
    let part1_time = watch.us();

    // part 2
    sums.sort();
    println!("{}", sums[sums.len() - 3..].iter().sum::<usize>());
    let part2_time = watch.us();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
