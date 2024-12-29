use aoc_shared::{get_input, report_times};
use simple_stopwatch::Stopwatch;

fn is_correct(update: &Vec<usize>, rules: &Vec<Vec<usize>>) -> bool {
    let mut is_correct = true;

    for rule in rules {
        let first_pos = update.iter().position(|&r| r == *rule.get(0).unwrap());
        let second_pos = update.iter().position(|&r| r == *rule.get(1).unwrap());

        if let (Some(first_index), Some(second_index)) = (first_pos, second_pos) {
            if first_index > second_index {
                is_correct = false;
            }
        }
    }

    return is_correct;
}

fn count_in_correct_updates(rules: &Vec<Vec<usize>>, updates: &Vec<Vec<usize>>) -> usize {
    let mut sum = 0;

    for update in updates {
        if is_correct(update, rules) {
            sum += update[(update.len() - 1) / 2];
        }
    }

    return sum;
}

fn count_in_fixed_updates(rules: &Vec<Vec<usize>>, updates: Vec<Vec<usize>>) -> usize {
    let mut sum = 0;

    for mut update in updates {
        if is_correct(&update, rules) {
            continue;
        }

        while !is_correct(&update, rules) {
            for rule in rules {
                let first = rule.get(0).unwrap();
                let second = rule.get(1).unwrap();
                let first_pos = update.iter().position(|&r| r == *first);
                let second_pos = update.iter().position(|&r| r == *second);

                if let (Some(first_index), Some(second_index)) = (first_pos, second_pos) {
                    if first_index > second_index {
                        update[first_index] = *second;
                        update[second_index] = *first;
                    }
                }
            }
        }
        sum += update[(update.len() - 1) / 2];
    }

    return sum;
}

fn main() {
    let watch = Stopwatch::start_new();

    // read and parse file
    let input = get_input("2024", "5", false).unwrap();
    let mut rules_processed = false;
    let mut rules: Vec<Vec<usize>> = Vec::new();
    let mut updates: Vec<Vec<usize>> = Vec::new();

    for line in input {
        let line = line.unwrap();
        if line.is_empty() {
            rules_processed = true;
            continue;
        }

        if !rules_processed {
            let rule = line
                .split("|")
                .map(|x| x.parse::<usize>().unwrap())
                .collect::<Vec<usize>>();
            rules.push(rule);
            continue;
        }

        let update = line
            .split(",")
            .map(|x| x.parse::<usize>().unwrap())
            .collect::<Vec<usize>>();
        updates.push(update);
    }
    let file_read_time = watch.us();

    // part 1
    println!("{}", count_in_correct_updates(&rules, &updates));
    let part1_time = watch.us();

    // part 2
    println!("{}", count_in_fixed_updates(&rules, updates));
    let part2_time = watch.us();

    // report times
    report_times(file_read_time, part1_time, part2_time);
}
