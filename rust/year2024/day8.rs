use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::{BufRead, BufReader};

use itertools::Itertools;
use simple_stopwatch::Stopwatch;

fn count_unique_antinodes(map: &Vec<Vec<char>>, find_all: bool) -> usize {
    let mut all_antennas: HashMap<char, Vec<(usize, usize)>> = HashMap::new();
    for i in 0..map.len() {
        for j in 0..map[0].len() {
            if map[i][j] == '.' { continue; }

            match all_antennas.get(&map[i][j]) {
                None => {
                    all_antennas.insert(map[i][j], vec![(i, j)]);
                }
                Some(_) => {
                    all_antennas.get_mut(&map[i][j]).unwrap().push((i, j));
                }
            }
        }
    }

    let mut antinodes: HashSet<(usize, usize)> = HashSet::new();
    for (_, antennas) in all_antennas.iter() {
        for antenna_pair in antennas.iter().combinations(2) {
            let nodes = find_antinodes(
                antenna_pair[0], antenna_pair[1],
                (map.len(), map[0].len()), find_all);
            for node in nodes {
                antinodes.insert(node);
            }
        }
    }

    antinodes.iter().count()
}

fn find_antinodes(
    antenna1: &(usize, usize),
    antenna2: &(usize, usize),
    map_size: (usize, usize),
    find_all: bool,
) -> Vec<(usize, usize)> {
    let antenna_distance_x = antenna2.0 as isize - antenna1.0 as isize;
    let antenna_distance_y = antenna2.1 as isize - antenna1.1 as isize;

    let mut antinodes: Vec<(usize, usize)> = vec![];
    let mut max_count: usize = 2;
    if find_all {
        antinodes.push(antenna1.clone());
        antinodes.push(antenna2.clone());
        max_count = map_size.0 * map_size.1;
    }

    let mut count: usize = 0;
    let mut x = antenna1.0 as isize;
    let mut y = antenna1.1 as isize;
    loop {
        if count >= max_count { break; }

        x -= antenna_distance_x;
        y -= antenna_distance_y;
        if x >= 0 && y >= 0 && x < map_size.0 as isize && y < map_size.1 as isize {
            antinodes.push((x as usize, y as usize));
        }
        count += 2;
    }

    count = 0;
    let mut x = antenna2.0 as isize;
    let mut y = antenna2.1 as isize;
    loop {
        if count >= max_count { break; }

        x += antenna_distance_x;
        y += antenna_distance_y;
        if x >= 0 && y >= 0 && x < map_size.0 as isize && y < map_size.1 as isize {
            antinodes.push((x as usize, y as usize));
        }
        count += 2;
    }

    antinodes
}

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let file = File::open("../inputs/2024/day8.txt").unwrap();
    let reader = BufReader::new(file);

    let map: Vec<Vec<char>> = reader.lines().map(
        |line| line.unwrap().chars().collect()
    ).collect();
    let file_read_time = watch.us();

    // part 1
    println!("{}", count_unique_antinodes(&map, false));
    let part1_time = watch.us() - file_read_time;

    // part 2
    println!("{}", count_unique_antinodes(&map, true));
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
