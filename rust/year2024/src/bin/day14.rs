use std::collections::HashSet;
use std::error::Error;
use std::fmt::{Display, Formatter, Result as FmtResult};
use std::fs::File;
use std::io::{BufReader, Lines};
use std::thread::sleep;
use std::time::{Duration, Instant};

use aoc_shared::{read_input, report_times};

#[derive(Clone, Eq, Hash, PartialEq)]
struct Robot {
    position: (isize, isize),
    velocity: (isize, isize),
}

impl Display for Robot {
    fn fmt(&self, f: &mut Formatter<'_>) -> FmtResult {
        write!(
            f,
            "Robot(position: ({}, {}), velocity: ({}, {}))",
            self.position.0, self.position.1, self.velocity.0, self.velocity.1
        )
    }
}

impl Robot {
    fn move_in_time(&mut self, map_size: (isize, isize), time_seconds: isize) {
        self.position = (
            (self.position.0 + self.velocity.0 * time_seconds).rem_euclid(map_size.0),
            (self.position.1 + self.velocity.1 * time_seconds).rem_euclid(map_size.1),
        );
    }
}

fn parse_input(input: Lines<BufReader<File>>) -> Result<Vec<Robot>, Box<dyn Error>> {
    let mut robots: Vec<Robot> = vec![];

    for line in input {
        let line = line?;
        if line.is_empty() {
            continue;
        }

        let parse = |s: &str| {
            let mut nums = s[2..].split(',').map(|n| n.parse().unwrap());
            (nums.next().unwrap(), nums.next().unwrap())
        };

        let mut parts = line.split_whitespace();
        if let (Some(p), Some(v)) = (parts.next(), parts.next()) {
            robots.push(Robot {
                position: parse(p),
                velocity: parse(v),
            });
        }
    }

    Ok(robots)
}

fn calculate_safety_factor(
    robots: &mut Vec<Robot>,
    map_size: (isize, isize),
    time_seconds: isize,
) -> isize {
    let mut quadrant_1: isize = 0;
    let mut quadrant_2: isize = 0;
    let mut quadrant_3: isize = 0;
    let mut quadrant_4: isize = 0;

    for robot in robots {
        robot.move_in_time(map_size, time_seconds);
        if robot.position.0 < map_size.0 / 2 && robot.position.1 < map_size.1 / 2 {
            quadrant_1 += 1;
        } else if robot.position.0 > map_size.0 / 2 && robot.position.1 < map_size.1 / 2 {
            quadrant_2 += 1;
        } else if robot.position.0 < map_size.0 / 2 && robot.position.1 > map_size.1 / 2 {
            quadrant_3 += 1;
        } else if robot.position.0 > map_size.0 / 2 && robot.position.1 > map_size.1 / 2 {
            quadrant_4 += 1;
        }
    }

    quadrant_1 * quadrant_2 * quadrant_3 * quadrant_4
}

fn print_map(robots: &Vec<Robot>, map_size: (isize, isize)) {
    for j in 0..map_size.1 {
        for i in 0..map_size.0 {
            let mut count = 0;
            for robot in robots {
                if robot.position == (i, j) {
                    count += 1;
                }
            }
            if count == 0 {
                print!(".");
            } else {
                print!("{}", count);
            }
        }
        println!();
        sleep(Duration::from_millis(10));
    }
    println!();
}

#[allow(dead_code)]
fn find_easter_egg_manually(robots: &mut Vec<Robot>, map_size: (isize, isize)) {
    for i in 1..1000 {
        for robot in robots.iter_mut() {
            robot.move_in_time(map_size, i);
        }
        println!("Second: {i}");
        print_map(&robots, map_size);
    }
}

fn find_easter_egg(robots: &mut Vec<Robot>, map_size: (isize, isize)) -> isize {
    let robots_len = robots.len();

    for i in 1..10000 {
        for robot in robots.iter_mut() {
            robot.move_in_time(map_size, 1);
        }

        let locations: HashSet<(isize, isize)> =
            robots.iter().map(|robot| robot.position).collect();
        if robots_len == locations.len() {
            return i;
        }
    }

    panic!("Could not find easter egg");
}

fn main() -> Result<(), Box<dyn Error>> {
    let start = Instant::now();

    // read and parse file
    let is_example: bool = false;
    let input = read_input("2024", "14", is_example)?;

    let mut robots: Vec<Robot> = parse_input(input)?;
    let mut map_size: (isize, isize) = (101, 103);
    if is_example {
        map_size = (11, 7);
    }
    let file_read_time = start.elapsed();

    // part 1
    let result: isize = calculate_safety_factor(&mut robots.clone(), map_size, 100);
    println!("{}", result);
    let part1_time = start.elapsed();

    // part 2
    // find_easter_egg_manually(&mut robots, map_size);
    let result: isize = find_easter_egg(&mut robots, map_size);
    println!("{}", result);
    let part2_time = start.elapsed();

    // report times
    report_times(file_read_time, part1_time, part2_time);
    Ok(())
}
