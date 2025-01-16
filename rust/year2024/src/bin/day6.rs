use std::collections::HashSet;
use std::io::{Error, ErrorKind};
use std::iter::Cycle;
use std::vec::IntoIter;

use simple_stopwatch::Stopwatch;

use aoc_shared::map::Map2D;
use aoc_shared::{get_input, report_times};

struct Library {
    map: Map2D<char>,
    guard: (isize, isize),
    direction: (isize, isize),
    history: HashSet<((isize, isize), (isize, isize))>,
}

impl Library {
    fn find_guard(map: &Map2D<char>) -> Result<((isize, isize), (isize, isize)), Error> {
        for x in 0..map.width() as isize {
            for y in 0..map.height() as isize {
                let element = map
                    .get_isize(x, y)
                    .expect("Could not get location from coordinates in library.");
                if !"<>^v".contains(*element) {
                    continue;
                }
                let direction: (isize, isize) = match element {
                    '>' => (1, 0),
                    '<' => (-1, 0),
                    '^' => (0, -1),
                    'v' => (0, 1),
                    _ => {
                        return Err(Error::new(
                            ErrorKind::InvalidInput,
                            "Guard facing direction not understood.",
                        ))
                    }
                };
                return Ok(((x, y), direction));
            }
        }
        Err(Error::new(ErrorKind::NotFound, "Guard not found."))
    }

    fn move_guard(&mut self) -> Result<(), Error> {
        let mut directions = self.create_direction_iterator();

        loop {
            match self.guard_make_step() {
                Ok(true) => continue,
                Ok(false) => {
                    self.direction = directions.next().expect("Could not get next direction.")
                }
                Err(err) => {
                    return Err(err);
                }
            };
        }
    }

    fn create_direction_iterator(&mut self) -> Cycle<IntoIter<(isize, isize)>> {
        let mut generator = vec![(1, 0), (0, 1), (-1, 0), (0, -1)].into_iter().cycle();
        while generator.next().unwrap() != self.direction {
            continue;
        }
        generator
    }

    fn guard_make_step(&mut self) -> Result<bool, Error> {
        if !self.history.insert((self.guard, self.direction)) {
            return Err(Error::new(ErrorKind::Interrupted, "Guard is in a loop."));
        }

        let (new_x, new_y) = (
            self.guard.0 + self.direction.0,
            self.guard.1 + self.direction.1,
        );

        match self.map.get_isize(new_x, new_y) {
            Some('#') => Ok(false),
            Some(_) => {
                self.guard = (new_x, new_y);
                Ok(true)
            }
            None => Err(Error::new(
                ErrorKind::InvalidInput,
                "Guard stepped outside of map.",
            )),
        }
    }

    fn get_unique_history_positions(&self) -> HashSet<(isize, isize)> {
        let mut unique_positions: HashSet<(isize, isize)> = HashSet::new();

        for (position, _) in &self.history {
            unique_positions.insert(*position);
        }

        unique_positions
    }

    fn count_obstacles_to_cause_loop(&mut self) -> usize {
        let original_guard_position = self.guard.clone();
        let original_guard_direction = self.direction.clone();

        let new_obstacle_positions = self.get_unique_history_positions();
        self.history.clear();

        let mut obstacles: usize = 0;
        for position in new_obstacle_positions {
            self.map.set_isize(position.0, position.1, '#');

            match self.move_guard() {
                Ok(_) => {}
                Err(err) => {
                    if err.kind() == ErrorKind::Interrupted {
                        obstacles += 1
                    }
                }
            }

            self.map.set_isize(position.0, position.1, '.');
            self.guard = original_guard_position.clone();
            self.direction = original_guard_direction.clone();
            self.history.clear();
        }

        obstacles
    }
}

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let input = get_input("2024", "6", false).unwrap();
    let map: Map2D<char> = Map2D::from_lines(input);
    let file_read_time = watch.us();

    // part 1
    let (guard_position, guard_direction) =
        Library::find_guard(&map).expect("Did not find guard in library.");

    let mut library = Library {
        map,
        guard: guard_position,
        direction: guard_direction,
        history: HashSet::new(),
    };
    let _ = library.move_guard();
    println!("{}", library.get_unique_history_positions().len());
    let part1_time = watch.us();

    // part 2
    library.direction = guard_direction;
    library.guard = guard_position;

    println!("{}", library.count_obstacles_to_cause_loop());
    let part2_time = watch.us();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
