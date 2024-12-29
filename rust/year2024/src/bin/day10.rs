use aoc_shared::{get_input, report_times};
use simple_stopwatch::Stopwatch;

fn get_score_and_rating(map: &Vec<Vec<usize>>) -> (usize, usize) {
    let mut score: usize = 0;
    let mut rating: usize = 0;

    for i in 0..map.len() {
        for j in 0..map[0].len() {
            let mut found_tops: Vec<(usize, usize)> = vec![];
            if map[i][j] != 0 {
                continue;
            }

            let mut to_expand: Vec<(usize, usize)> = vec![(i, j)];
            while !to_expand.is_empty() {
                let position = to_expand.pop().unwrap();
                let level = map[position.0][position.1];
                if level == 9 {
                    if !found_tops.contains(&position) {
                        score += 1;
                        found_tops.push(position);
                    }
                    rating += 1;
                    continue;
                }
                for neighbor in get_neighbors_on_slope(position, level + 1, map) {
                    to_expand.push(neighbor);
                }
            }
        }
    }

    (score, rating)
}

fn get_neighbors_on_slope(
    position: (usize, usize),
    level: usize,
    map: &Vec<Vec<usize>>,
) -> Vec<(usize, usize)> {
    let map_x_size = map.len();
    let map_y_size = map[0].len();
    let mut valid_neighbors: Vec<(usize, usize)> = vec![];

    if position.0 > 0 && map[position.0 - 1][position.1] == level {
        valid_neighbors.push((position.0 - 1, position.1));
    }
    if position.0 < map_x_size - 1 && map[position.0 + 1][position.1] == level {
        valid_neighbors.push((position.0 + 1, position.1));
    }
    if position.1 > 0 && map[position.0][position.1 - 1] == level {
        valid_neighbors.push((position.0, position.1 - 1));
    }
    if position.1 < map_y_size - 1 && map[position.0][position.1 + 1] == level {
        valid_neighbors.push((position.0, position.1 + 1));
    }

    valid_neighbors
}

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let input = get_input("2024", "10", false).unwrap();
    let mut map: Vec<Vec<usize>> = vec![];

    for line in input {
        let line = line.unwrap();
        if line.is_empty() {
            continue;
        }

        let mut row: Vec<usize> = vec![];
        for char in line.chars() {
            row.push(char.to_digit(10).unwrap() as usize);
        }
        map.push(row);
    }
    let file_read_time = watch.us();

    // part 1
    let (score, rating) = get_score_and_rating(&map);
    println!("{}", score);
    let part1_time = watch.us();

    // part 2
    println!("{}", rating);
    let part2_time = watch.us();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
