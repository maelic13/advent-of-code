use std::error::Error;
use std::time::Instant;

use aoc_shared::{read_input, report_times};

fn parse_coordinates(input: &str) -> (isize, isize) {
    let mut parts = input.split(',');
    let x_str = parts
        .next()
        .unwrap()
        .trim()
        .split_once(['=', '+'])
        .unwrap()
        .1;
    let y_str = parts
        .next()
        .unwrap()
        .trim()
        .split_once(['=', '+'])
        .unwrap()
        .1;

    let x = x_str.parse().unwrap();
    let y = y_str.parse().unwrap();

    (x, y)
}

fn solve_coordinates(
    treasure: &(isize, isize),
    a_button: &(isize, isize),
    b_button: &(isize, isize),
) -> Option<(isize, isize)> {
    let det = a_button.0 * b_button.1 - a_button.1 * b_button.0;

    if det == 0 {
        // no unique solution (linearly dependent vectors)
        return None;
    }

    let n_f = (b_button.1 * treasure.0 - b_button.0 * treasure.1) as f64 / det as f64;
    let m_f = (-a_button.1 * treasure.0 + a_button.0 * treasure.1) as f64 / det as f64;

    let m = n_f.round() as isize;
    let n = m_f.round() as isize;

    if !(m * a_button.0 + n * b_button.0 == treasure.0
        && m * a_button.1 + n * b_button.1 == treasure.1)
    {
        // no integer solution (rounding error)
        return None;
    }

    Some((m, n))
}

fn calculate_price_for_all_possible_treasures(
    machines: &Vec<((isize, isize), (isize, isize), (isize, isize))>,
    add_coordinates: bool,
) -> isize {
    let mut cost: isize = 0;

    for (a_button, b_button, treasure) in machines {
        let mut fixed_treasure = *treasure;
        if add_coordinates {
            fixed_treasure = (treasure.0 + 10000000000000, treasure.1 + 10000000000000);
        }

        match solve_coordinates(&fixed_treasure, a_button, b_button) {
            Some((a_pushes, b_pushes)) => {
                cost += a_pushes * 3 + b_pushes;
            }
            None => continue,
        }
    }

    cost
}

fn main() -> Result<(), Box<dyn Error>> {
    let start = Instant::now();

    // read and parse file
    let input = read_input("2024", "13", false)?;
    let mut machines: Vec<((isize, isize), (isize, isize), (isize, isize))> = vec![];

    let mut a_button: (isize, isize) = (0, 0);
    let mut b_button: (isize, isize) = (0, 0);

    for (i, line) in input.into_iter().enumerate() {
        let line = line?;
        if line.is_empty() {
            continue;
        }

        match i % 4 {
            0 => a_button = parse_coordinates(&line),
            1 => b_button = parse_coordinates(&line),
            _ => machines.push((a_button, b_button, parse_coordinates(&line))),
        }
    }
    let file_read_time = start.elapsed();

    // part 1
    let result: isize = calculate_price_for_all_possible_treasures(&machines, false);
    println!("{result}");
    let part1_time = start.elapsed();

    // part 2
    let result: isize = calculate_price_for_all_possible_treasures(&machines, true);
    println!("{result}");
    let part2_time = start.elapsed();

    // report times
    report_times(file_read_time, part1_time, part2_time);
    Ok(())
}
