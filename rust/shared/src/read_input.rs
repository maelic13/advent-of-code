use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader, Lines};

const INPUT_PATH: &str = "D:/Code/advent-of-code/inputs";

pub fn read_input(
    year: &str,
    day: &str,
    example: bool,
) -> Result<Lines<BufReader<File>>, Box<dyn Error>> {
    let mut suffix: &str = "";
    if example {
        suffix = "_ex";
    }

    let file = File::open(format!("{}/{}/day{}{}.txt", INPUT_PATH, year, day, suffix))?;
    let reader = BufReader::new(file);
    Ok(reader.lines())
}
