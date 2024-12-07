use std::cmp::PartialEq;
use std::fs::File;
use std::io::{BufRead, BufReader, Error, ErrorKind};

use simple_stopwatch::Stopwatch;

#[derive(Debug)]
struct Position {
    x: usize,
    y: usize,
}

struct Library {
    map: Vec<Vec<char>>,
    guard: Position,
    history: Vec<(Position, char)>,
}

impl Position {
    fn new(position: &Position) -> Position {
        Position { x: position.x, y: position.y }
    }

    fn from_tuple(t: (isize, isize)) -> Position {
        Position { x: t.0 as usize, y: t.1 as usize }
    }
}

impl PartialEq<Position> for &Position {
    fn eq(&self, other: &Position) -> bool {
        &self.x == &other.x && &self.y == &other.y
    }
}

impl Library {
    fn find_guard(map: &Vec<Vec<char>>) -> Result<Position, Error> {
        for x in 0..map.len() {
            for y in 0..map[0].len() {
                if "<>^v".contains(map[x][y]) {
                    return Ok(Position { x, y });
                }
            }
        }
        Err(Error::new(ErrorKind::NotFound, "Guard not found."))
    }

    fn move_guard(&mut self) -> Result<(), Error> {
        loop {
            match self.guard_make_step() {
                Ok(true) => continue,
                Ok(false) => self.rotate_guard(),
                Err(err) => {
                    return Err(err);
                }
            };
        }
    }

    fn rotate_guard(&mut self) {
        let right_rotation = ">v<^>";
        let guard_direction = self.map[self.guard.x][self.guard.y];

        let guard_direction_index = right_rotation.find(guard_direction).unwrap();
        self.map[self.guard.x][self.guard.y] = right_rotation.chars().nth(
            guard_direction_index + 1
        ).unwrap();
    }

    fn guard_make_step(&mut self) -> Result<bool, Error> {
        if self.find_in_history(&self.guard, self.map[self.guard.x][self.guard.y]) {
            return Err(Error::new(
                ErrorKind::Interrupted, "Guard is in a loop.")
            );
        }
        self.history.push((Position::new(&self.guard), self.map[self.guard.x][self.guard.y]));

        let direction: (isize, isize) = match self.map[self.guard.x][self.guard.y] {
            '>' => (0, 1),
            '<' => (0, -1),
            '^' => (-1, 0),
            'v' => (1, 0),
            _ => return Err(Error::new(
                ErrorKind::InvalidInput, "Guard facing direction not understood.")
            ),
        };

        let new_guard_position = (self.guard.x as isize + direction.0, self.guard.y as isize + direction.1);
        if new_guard_position.0 < 0 || new_guard_position.0 >= self.map.len() as isize
            || new_guard_position.1 < 0 || new_guard_position.1 >= self.map[0].len() as isize {
            self.map[self.guard.x][self.guard.y] = 'X';
            return Err(Error::new(
                ErrorKind::InvalidInput, "Guard stepped outside of map.")
            );
        }

        let new_guard_position = Position::from_tuple(new_guard_position);
        if self.map[new_guard_position.x][new_guard_position.y] == '#' {
            return Ok(false);
        }

        self.map[new_guard_position.x][new_guard_position.y] = self.map[self.guard.x][self.guard.y];
        self.map[self.guard.x][self.guard.y] = 'X';
        self.guard = new_guard_position;
        Ok(true)
    }

    fn count_guard_route(&mut self) -> usize {
        let mut count: usize = 0;
        for x in 0..self.map.len() {
            for y in 0..self.map[0].len() {
                if self.map[x][y] == 'X' { count += 1; }
            }
        }
        count
    }

    fn find_in_history(&self, position: &Position, direction: char) -> bool {
        for (h_position, h_direction) in &self.history {
            if position == *h_position && direction == *h_direction { return true; }
        }
        false
    }

    fn count_obstacles_to_cause_loop(&mut self) -> usize {
        let original_map = self.map.to_vec();
        let original_guard = Position{ x: self.guard.x, y: self.guard.y };
        let mut obstacles: usize = 0;

        for x in 0..self.map.len() {
            for y in 0..self.map[0].len() {
                if self.map[x][y] != 'X' { continue; }

                self.map[x][y] = '#';
                match self.move_guard() {
                    Ok(_) => {},
                    Err(err) => {
                        if err.kind() == ErrorKind::Interrupted { obstacles += 1 }
                    }
                }
                self.map = original_map.to_vec();
                self.guard = Position{ x: original_guard.x, y: original_guard.y };
                self.history = vec![];
            }
        }
        obstacles
    }
}

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let file = File::open("../inputs/2024/day6.txt").unwrap();
    let reader = BufReader::new(file);
    let mut map: Vec<Vec<char>> = vec![];

    for line in reader.lines() {
        let line = line.unwrap();
        if line.is_empty() { continue; }

        map.push(line.chars().collect());
    }
    let file_read_time = watch.us();

    // part 1
    let guard_position = Library::find_guard(&map).unwrap();
    let guard_direction = map[guard_position.x][guard_position.y];

    let mut library = Library { map, guard: Position::new(&guard_position), history: vec![] };
    let _ = library.move_guard();
    println!("{}", library.count_guard_route());
    let part1_time = watch.us() - file_read_time;

    // part 2
    library.map[guard_position.x][guard_position.y] = guard_direction;
    library.guard = guard_position;
    library.history = vec![];
    
    println!("{}", library.count_obstacles_to_cause_loop());
    let part2_time = watch.us() - part1_time - file_read_time;

    // report times
    println!();
    println!("Total time: {:.1} seconds.", watch.us() / 1_000_000.);
    println!("File read time: {:.0} microseconds.", file_read_time);
    println!(
        "Execution time: {:.1} seconds.",
        (part1_time + part2_time) / 1_000_000.
    );
    println!();
    println!("Part 1 execution time: {:.0} milliseconds.", part1_time / 1_000.);
    println!("Part 2 execution time: {:.01} seconds.", part2_time / 1_000_000.);
}
