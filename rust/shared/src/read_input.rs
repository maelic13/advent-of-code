use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader, Lines};
use std::path::{Path, PathBuf};

fn get_input_path() -> PathBuf {
    let manifest_dir = Path::new(env!("CARGO_MANIFEST_DIR"));
    let workspace_root = manifest_dir
        .parent()
        .and_then(|p| p.parent())
        .unwrap_or_else(|| Path::new("."))
        .to_owned();

    workspace_root.join("inputs")
}

pub fn read_input(
    year: &str,
    day: &str,
    example: bool,
) -> Result<Lines<BufReader<File>>, Box<dyn Error>> {
    let mut suffix: &str = "";
    if example {
        suffix = "_ex";
    }

    let file_path = get_input_path().join(format!("{}/day{}{}.txt", year, day, suffix));
    let file = File::open(&file_path)?;
    let reader = BufReader::new(file);
    Ok(reader.lines())
}
