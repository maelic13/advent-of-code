use std::collections::HashMap;
use std::error::Error;
use std::time::Instant;

use aoc_shared::{Map2D, read_input, report_times};

fn find_start(map: &Map2D<char>) -> (usize, usize) {
    for i in 0..map.width() {
        if *map.get(i, 0) == 'S' {
            return (i, 0);
        }
    }
    panic!("Could not find start.")
}

fn count_splits(start_position: (usize, usize), map: &Map2D<char>) -> usize {
    let mut active_beams: Vec<bool> = vec![false; map.width()];
    active_beams[start_position.0] = true;

    let mut splits: usize = 0;
    for y in 1..map.height() {
        for x in 0..map.width() {
            if *map.get(x, y) == '^' && active_beams[x] {
                splits += 1;
                active_beams[x] = false;
                active_beams[x + 1] = true;
                active_beams[x - 1] = true;
            }
        }
    }

    splits
}

fn count_realities(
    beam_position: (usize, usize),
    map: &Map2D<char>,
    cache: &mut HashMap<(usize, usize), usize>,
) -> usize {
    if let Some(&count) = cache.get(&beam_position) {
        return count;
    }

    if beam_position.1 >= map.height() - 1 {
        cache.insert(beam_position, 1);
        return 1;
    }

    let mut count: usize = 0;
    for node in expand_node(beam_position, map) {
        count += count_realities(node, map, cache);
    }
    cache.insert(beam_position, count);
    count
}

fn expand_node(node: (usize, usize), map: &Map2D<char>) -> Vec<(usize, usize)> {
    if *map.get(node.0, node.1) != '^' {
        return vec![(node.0, node.1 + 1)];
    }
    vec![(node.0 + 1, node.1 + 1), (node.0 - 1, node.1 + 1)]
}

fn main() -> Result<(), Box<dyn Error>> {
    let start = Instant::now();

    // read and parse file
    let input = read_input("2025", "7", false)?;
    let map: Map2D<char> = Map2D::from_lines(input);
    let start_position = find_start(&map);
    let file_read_time = start.elapsed();

    // part 1
    let part1_result: usize = count_splits(start_position, &map);
    let part1_time = start.elapsed();

    // part 2
    let mut cache: HashMap<(usize, usize), usize> = HashMap::new();
    let part2_result: usize = count_realities(start_position, &map, &mut cache);
    let part2_time = start.elapsed();

    // report results and times
    println!("{part1_result}");
    println!("{part2_result}");
    report_times(file_read_time, part1_time, part2_time);
    Ok(())
}
