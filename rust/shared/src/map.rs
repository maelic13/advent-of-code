use std::fmt::Display;
use std::fs::File;
use std::io::{BufReader, Lines};

pub struct Map2D<T> {
    data: Vec<T>,
    width: usize,
    height: usize,
}

impl<T: Display> Map2D<T> {
    pub fn index(&self, x: usize, y: usize) -> usize {
        y * self.width + x
    }

    pub fn get(&self, x: usize, y: usize) -> Option<&T> {
        if x >= self.height || y >= self.width {
            return None;
        }
        self.data.get(self.index(x, y))
    }

    pub fn get_isize(&self, x: isize, y: isize) -> Option<&T> {
        if x < 0 || y < 0 {
            return None;
        }
        self.get(x as usize, y as usize)
    }

    pub fn print_map(&self) {
        for row in 0..self.height {
            for col in 0..self.width {
                print!("{} ", self.data[row * self.width + col]);
            }
            println!();
        }
        println!();
    }

    pub fn width(&self) -> usize {
        self.width
    }

    pub fn height(&self) -> usize {
        self.height
    }
}

pub trait FromLines: Sized {
    fn from_lines(lines: Lines<BufReader<File>>) -> Self;
}

impl FromLines for Map2D<String> {
    fn from_lines(lines: Lines<BufReader<File>>) -> Self {
        let mut data: Vec<String> = vec![];
        let mut width: usize = 0;
        let mut height: usize = 0;

        for line in lines {
            let line = line.expect("Failed to read line");
            if line.is_empty() {
                continue;
            }

            height += 1;
            width = line.len();

            for char in line.chars() {
                data.push(String::from(char));
            }
        }

        Map2D {
            data,
            width,
            height,
        }
    }
}

impl FromLines for Map2D<isize> {
    fn from_lines(lines: Lines<BufReader<File>>) -> Self {
        let mut data: Vec<isize> = vec![];
        let mut width: usize = 0;
        let mut height: usize = 0;

        for line in lines {
            let line = line.expect("Failed to read line");
            if line.is_empty() {
                continue;
            }

            height += 1;
            width = line.len();

            for char in line.chars() {
                data.push(char.to_digit(10).expect("Could not parse char into digit.") as isize);
            }
        }

        Map2D {
            data,
            width,
            height,
        }
    }
}
