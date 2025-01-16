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
        // To get number of sides, calculate sum of corners in area.
        let mut number_of_sides: usize = 0;

        for plot in self.plots.iter() {
            number_of_sides += self.convex(plot) + self.concave(plot);
        }

        number_of_sides
    }

    fn contains(&self, coordinates: (isize, isize)) -> bool {
        if coordinates.0 < 0 || coordinates.1 < 0 {
            return false;
        }

        self.plots.contains(&(coordinates.0 as usize, coordinates.1 as usize))
    }

    fn convex(&self, plot: &(usize, usize)) -> usize {
        let mut num: usize = 0;

        let up: (isize, isize) = (plot.0 as isize - 1, plot.1 as isize);
        let down: (isize, isize) = (plot.0 as isize + 1, plot.1 as isize);
        let left: (isize, isize) = (plot.0 as isize, plot.1 as isize - 1);
        let right: (isize, isize) = (plot.0 as isize, plot.1 as isize + 1);

        if !self.contains(up) && !self.contains(right) {
            num += 1;
        }

        if !self.contains(right) && !self.contains(down) {
            num += 1;
        }

        if !self.contains(down) && !self.contains(left) {
            num += 1;
        }

        if !self.contains(left) && !self.contains(up) {
            num += 1;
        }

        num
    }

    fn concave(&self, plot: &(usize, usize)) -> usize {
        let mut num: usize = 0;

        let up: (isize, isize) = (plot.0 as isize - 1, plot.1 as isize);
        let down: (isize, isize) = (plot.0 as isize + 1, plot.1 as isize);
        let left: (isize, isize) = (plot.0 as isize, plot.1 as isize - 1);
        let right: (isize, isize) = (plot.0 as isize, plot.1 as isize + 1);
        let up_right: (isize, isize) = (plot.0 as isize - 1, plot.1 as isize + 1);
        let up_left: (isize, isize) = (plot.0 as isize - 1, plot.1 as isize - 1);
        let down_right: (isize, isize) = (plot.0 as isize + 1, plot.1 as isize + 1);
        let down_left: (isize, isize) = (plot.0 as isize + 1, plot.1 as isize - 1);

        if self.contains(up) && self.contains(right) && !self.contains(up_right) {
            num += 1;
        }

        if self.contains(right) && self.contains(down) && !self.contains(down_right) {
            num += 1;
        }

        if self.contains(down) && self.contains(left) && !self.contains(down_left) {
            num += 1;
        }

        if self.contains(left) && self.contains(up) && !self.contains(up_left) {
            num += 1;
        }

        num
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
    let input = get_input("2024", "12", false).unwrap();
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
