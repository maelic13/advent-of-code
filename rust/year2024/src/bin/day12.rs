use simple_stopwatch::Stopwatch;
use std::collections::HashSet;

use aoc_shared::map::Map2D;
use aoc_shared::{get_input, report_times};

struct Area {
    plots: HashSet<(isize, isize)>,
}

impl Area {
    fn perimeter(&self) -> usize {
        let mut perimeter: usize = 0;
        let directions: Vec<(isize, isize)> = vec![(0, -1), (0, 1), (1, 0), (-1, 0)];

        for plot in &self.plots {
            for direction in &directions {
                let to_check = (plot.0 + direction.0, plot.1 + direction.1);

                if !self.plots.contains(&to_check) {
                    perimeter += 1;
                }
            }
        }
        perimeter
    }

    fn number_of_sides(&self) -> usize {
        // To get number of sides, calculate sum of corners in area.
        let mut number_of_sides: usize = 0;

        for plot in self.plots.iter() {
            number_of_sides += self.convex(plot) + self.concave(plot);
        }

        number_of_sides
    }

    fn convex(&self, plot: &(isize, isize)) -> usize {
        let mut num: usize = 0;

        let up: (isize, isize) = (plot.0 - 1, plot.1);
        let down: (isize, isize) = (plot.0 + 1, plot.1);
        let left: (isize, isize) = (plot.0, plot.1 - 1);
        let right: (isize, isize) = (plot.0, plot.1 + 1);

        if !self.plots.contains(&up) && !self.plots.contains(&right) {
            num += 1;
        }

        if !self.plots.contains(&right) && !self.plots.contains(&down) {
            num += 1;
        }

        if !self.plots.contains(&down) && !self.plots.contains(&left) {
            num += 1;
        }

        if !self.plots.contains(&left) && !self.plots.contains(&up) {
            num += 1;
        }

        num
    }

    fn concave(&self, plot: &(isize, isize)) -> usize {
        let mut num: usize = 0;

        let up: (isize, isize) = (plot.0 - 1, plot.1);
        let down: (isize, isize) = (plot.0 + 1, plot.1);
        let left: (isize, isize) = (plot.0, plot.1 - 1);
        let right: (isize, isize) = (plot.0, plot.1 + 1);
        let up_right: (isize, isize) = (plot.0 - 1, plot.1 + 1);
        let up_left: (isize, isize) = (plot.0 - 1, plot.1 - 1);
        let down_right: (isize, isize) = (plot.0 + 1, plot.1 + 1);
        let down_left: (isize, isize) = (plot.0 + 1, plot.1 - 1);

        if self.plots.contains(&up)
            && self.plots.contains(&right)
            && !self.plots.contains(&up_right)
        {
            num += 1;
        }

        if self.plots.contains(&right)
            && self.plots.contains(&down)
            && !self.plots.contains(&down_right)
        {
            num += 1;
        }

        if self.plots.contains(&down)
            && self.plots.contains(&left)
            && !self.plots.contains(&down_left)
        {
            num += 1;
        }

        if self.plots.contains(&left) && self.plots.contains(&up) && !self.plots.contains(&up_left)
        {
            num += 1;
        }

        num
    }

    fn fence_cost(&self) -> usize {
        self.perimeter() * self.plots.len()
    }

    fn fence_cost_discounted(&self) -> usize {
        self.number_of_sides() * self.plots.len()
    }
}

fn find_areas(map: &Map2D<char>) -> Vec<Area> {
    let mut areas: Vec<Area> = vec![];
    let mut already_found_positions: HashSet<(isize, isize)> = HashSet::new();

    for i in 0..map.height() as isize {
        for j in 0..map.width() as isize {
            if already_found_positions.contains(&(i, j)) {
                continue;
            }
            let plant = map
                .get_isize(i, j)
                .expect("Getting element from map failed.");
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
    map: &Map2D<char>,
    initial_position: (isize, isize),
    plant: &char,
) -> Area {
    let mut plots: HashSet<(isize, isize)> = HashSet::from([initial_position]);
    let directions_to_check: Vec<(isize, isize)> = vec![(-1, 0), (1, 0), (0, -1), (0, 1)];
    let mut to_check: Vec<(isize, isize)> = vec![initial_position];

    while !to_check.is_empty() {
        let position = to_check
            .pop()
            .expect("Could not get position to check from vector.");
        if map
            .get_isize(position.0, position.1)
            .expect("Could not get plant from position in map.")
            != plant
        {
            continue;
        }

        for direction in &directions_to_check {
            let new_position = (position.0 + direction.0, position.1 + direction.1);
            if plots.contains(&new_position) {
                continue;
            }

            let new_plant: &char;
            match map.get_isize(new_position.0, new_position.1) {
                Some(found_plant) => new_plant = found_plant,
                None => continue,
            }
            if new_plant != plant {
                continue;
            }

            plots.insert(new_position);
            to_check.push(new_position);
        }
    }

    Area { plots }
}

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let input = get_input("2024", "12", false).unwrap();
    let map: Map2D<char> = Map2D::from_lines(input);
    let file_read_time = watch.us();

    // part 1
    let areas = find_areas(&map);
    println!(
        "{}",
        areas.iter().map(|area| area.fence_cost()).sum::<usize>()
    );
    let part1_time = watch.us();

    // part 2
    println!(
        "{}",
        areas
            .iter()
            .map(|area| area.fence_cost_discounted())
            .sum::<usize>()
    );
    let part2_time = watch.us();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
