use std::time::Duration;

pub fn report_times(file_parse_time: Duration, part1_time: Duration, part2_time: Duration) {
    let execution_time = part2_time.saturating_sub(file_parse_time);
    let only_part1_time = part1_time.saturating_sub(file_parse_time);
    let only_part2_time = part2_time.saturating_sub(part1_time);

    println!();
    println!("Total time: {part2_time:#.1?}.");
    println!("File read time: {file_parse_time:#.1?}.");
    println!("Execution time: {execution_time:#.1?}.");
    println!();
    println!("Part 1 execution time: {only_part1_time:#.1?}.");
    println!("Part 2 execution time: {only_part2_time:#.1?}.");
}
