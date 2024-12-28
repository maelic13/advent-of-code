use std::fmt::Display;
use std::fs::File;
use std::io::{BufReader, Lines};

pub trait ParseElement: Sized {
    fn parse_element(token: char) -> Self;
}

impl ParseElement for i32 {
    fn parse_element(token: char) -> Self {
        token.to_digit(10).expect("Failed to parse i32.") as i32
    }
}

impl ParseElement for String {
    fn parse_element(token: char) -> Self {
        token.to_string()
    }
}

pub struct Map<T> {
    data: Vec<T>,
    width: usize,
    height: usize,
}

impl<T> Map<T> {
    pub fn get(&self, row: usize, col: usize) -> Option<&T> {
        if row < self.height && col < self.width {
            self.data.get(row * self.width + col)
        } else {
            None
        }
    }
}

impl<T: ParseElement> Map<T> {
    pub fn from_lines(lines: Lines<BufReader<File>>) -> Self {
        let mut data = Vec::new();
        let mut width: usize = 0;
        let mut height = 0;

        for line in lines {
            let line = line.unwrap();
            if line.is_empty() {
                continue;
            }

            height += 1;
            width = line.len();

            for char in line.chars() {
                data.push(ParseElement::parse_element(char));
            }
        }

        Map {
            data,
            width,
            height,
        }
    }
}

impl<T> Map<T>
where
    T: Display,
{
    pub fn print_map(&self) {
        for row in 0..self.height {
            for col in 0..self.width {
                // Use Display trait to print each element with a space
                print!("{} ", self.data[row * self.width + col]);
            }
            println!();
        }
        println!();
    }
}

pub struct IntMap {
    map: Map<i32>,
}

impl IntMap {
    pub fn from_lines(lines: Lines<BufReader<File>>) -> Self {
        Self {
            map: Map::from_lines(lines),
        }
    }

    pub fn width(&self) -> usize {
        self.map.width
    }
    pub fn height(&self) -> usize {
        self.map.height
    }

    pub fn get(&self, row: usize, col: usize) -> Option<i32> {
        self.map.get(row, col).copied()
    }

    pub fn print_map(&self) {
        self.map.print_map();
    }
}

pub struct StringMap {
    map: Map<String>,
}

impl StringMap {
    pub fn from_lines(lines: Lines<BufReader<File>>) -> Self {
        Self {
            map: Map::from_lines(lines),
        }
    }

    pub fn width(&self) -> usize {
        self.map.width
    }
    pub fn height(&self) -> usize {
        self.map.height
    }

    pub fn get(&self, row: usize, col: usize) -> Option<String> {
        Some(self.map.get(row, col).unwrap().to_string())
    }

    pub fn get_isize(&self, row: isize, col: isize) -> Option<String> {
        if row < 0 || col < 0 {
            return None;
        }

        match self.map.get(row as usize, col as usize) {
            Some(v) => Some(v.to_string()),
            None => None,
        }
    }

    pub fn print_map(&self) {
        self.map.print_map();
    }
}
