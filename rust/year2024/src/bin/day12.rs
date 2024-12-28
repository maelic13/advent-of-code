use aoc_shared::map::StringMap;
use aoc_shared::{get_input, report_times};
use simple_stopwatch::Stopwatch;
use std::collections::HashSet;

struct Area {
    plots: HashSet<(usize, usize)>,
}

impl Area {
    fn perimeter(&self) -> usize {
        let mut perimeter: usize = 0;
        let directions: Vec<(isize, isize)> = vec![(0, -1), (0, 1), (1, 0), (-1, 0)];

        for plot in &self.plots {
            for direction in &directions {
                let to_check = (plot.0 as isize + direction.0, plot.1 as isize + direction.1);

                if to_check.0 < 0
                    || to_check.1 < 0
                    || !self
                        .plots
                        .contains(&(to_check.0 as usize, to_check.1 as usize))
                {
                    perimeter += 1;
                }
            }
        }
        perimeter
    }

    fn number_of_sides(&self) -> usize {
        println!("Plots: {:?}", self.plots);
        let directions: Vec<(isize, isize)> = vec![(0, -1), (1, 0), (0, 1), (-1, 0)];
        let mut number_of_sides: usize = 0;

        // find top-left element
        let min_x: &usize = &self.plots.iter().map(|x| x.0).min().unwrap();
        let min_y: &usize = &self
            .plots
            .iter()
            .filter_map(|x| if x.0 == *min_x { Some(x.1) } else { None })
            .min()
            .unwrap();
        let start: (usize, usize) = (*min_x, *min_y);
        println!("Start: {:?}", start);

        let mut current_position: (usize, usize) = start.clone();
        let mut current_direction: (isize, isize) = (0, -1);
        let mut visited: HashSet<(usize, usize)> = HashSet::from([current_position]);
        loop {
            println!("Current position: {:?}", current_position);
            let mut new_position = (current_position.0 as isize, current_position.1 as isize);
            for direction in &directions {
                new_position = (
                    current_position.0 as isize + direction.0,
                    current_position.1 as isize + direction.1,
                );
                println!(
                    "New position: {:?}, current direction: {:?}",
                    new_position, current_direction
                );
                if new_position.0 < 0
                    || new_position.1 < 0
                    || visited.contains(&(new_position.0 as usize, new_position.1 as usize))
                    || !self
                        .plots
                        .contains(&(new_position.0 as usize, new_position.1 as usize))
                {
                    continue;
                }

                if &current_direction != direction {
                    number_of_sides += 1;
                }
                current_direction = *direction;
                break;
            }
            if current_position == (new_position.0 as usize, new_position.1 as usize) {
                break;
            }
            current_position = (new_position.0 as usize, new_position.1 as usize);
            visited.insert((current_position.0, current_position.1));
            if current_position == start {
                break;
            }
        }

        number_of_sides
    }

    fn calculate_fence_cost(&self) -> usize {
        self.perimeter() * self.plots.len()
    }

    fn calculate_cost_discounted(&self) -> usize {
        self.number_of_sides() * self.plots.len()
    }
}

fn find_areas(map: &StringMap) -> Vec<Area> {
    let mut areas: Vec<Area> = vec![];
    let mut already_found_positions: HashSet<(usize, usize)> = HashSet::new();

    for i in 0..map.height() {
        for j in 0..map.width() {
            if already_found_positions.contains(&(i, j)) {
                continue;
            }
            let plant = map.get(i, j).unwrap();
            let area: Area = find_area_from_position(map, (i, j), plant);
            for position in &area.plots {
                already_found_positions.insert(*position);
            }
            areas.push(area);
        }
    }
    areas
}

fn find_area_from_position(
    map: &StringMap,
    initial_position: (usize, usize),
    plant: String,
) -> Area {
    let mut plots: HashSet<(usize, usize)> = HashSet::from([initial_position]);
    let directions_to_check: Vec<(isize, isize)> = vec![(-1, 0), (1, 0), (0, -1), (0, 1)];
    let mut to_check: Vec<(usize, usize)> = vec![initial_position];

    while !to_check.is_empty() {
        let position = to_check.pop().unwrap();
        if map.get(position.0, position.1).unwrap() != plant {
            continue;
        }

        for direction in &directions_to_check {
            let new_position = (
                position.0 as isize + direction.0,
                position.1 as isize + direction.1,
            );
            if plots.contains(&(new_position.0 as usize, new_position.1 as usize)) {
                continue;
            }

            let new_plant: String;
            match map.get_isize(new_position.0, new_position.1) {
                Some(found_plant) => new_plant = found_plant,
                None => continue,
            }
            if new_plant != plant {
                continue;
            }

            plots.insert((new_position.0 as usize, new_position.1 as usize));
            to_check.push((new_position.0 as usize, new_position.1 as usize));
        }
    }

    Area { plots }
}

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let input = get_input("2024", "12", true).unwrap();
    let map = StringMap::from_lines(input);
    let file_read_time = watch.us();

    // part 1
    let areas = find_areas(&map);
    println!(
        "{}",
        areas
            .iter()
            .map(|area| area.calculate_fence_cost())
            .sum::<usize>()
    );
    let part1_time = watch.us();

    // part 2
    println!(
        "{}",
        areas
            .iter()
            .map(|area| area.calculate_cost_discounted())
            .sum::<usize>()
    );
    let part2_time = watch.us();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
