use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader, Lines};

pub mod map;

const INPUT_PATH: &str = "D:/Code/advent-of-code/inputs";

pub fn get_input(
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

pub fn report_times(file_parse_time: f32, part1_time: f32, part2_time: f32) {
    fn check_time(time: f32) -> String {
        if time < 1_000. {
            return format!("{:.0} microseconds", time);
        }

        let mut modified_time = time / 1_000.;
        if modified_time < 1_000. {
            return format!("{:.1} milliseconds", modified_time);
        }

        modified_time /= 1_000.;
        if modified_time < 60. {
            return format!("{:.1} seconds", modified_time);
        }

        modified_time /= 60.;
        if modified_time < 60. {
            return format!(
                "{:.0} minutes, {:.0} seconds",
                modified_time,
                modified_time * 60. % 60.
            );
        }

        modified_time /= 60.;
        if modified_time < 60. {
            return format!(
                "{:.0} hours, {:.0} minutes",
                modified_time,
                modified_time * 60. % 60.
            );
        }

        "I am not calculating runtime in days! Forget it and fix your code!".to_string()
    }

    println!();
    println!("Total time: {}.", check_time(part2_time));
    println!("File read time: {}.", check_time(file_parse_time));
    println!(
        "Execution time: {}.",
        check_time(part2_time - file_parse_time)
    );
    println!();
    println!(
        "Part 1 execution time: {}.",
        check_time(part1_time - file_parse_time)
    );
    println!(
        "Part 2 execution time: {}.",
        check_time(part2_time - part1_time)
    );
}
