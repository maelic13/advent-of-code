extern crate core;

use std::fs::File;
use std::io::{BufReader, BufRead};

use simple_stopwatch::Stopwatch;


pub struct RPSPlayer {
    pub win_score: usize,
    pub draw_score: usize,
    pub lose_score: usize,

    pub rock_score: usize,
    pub paper_score: usize,
    pub scissors_score: usize,

    pub wins: Vec<Vec<String>>,
    pub draws: Vec<Vec<String>>,
    pub losses: Vec<Vec<String>>,
}

impl RPSPlayer {
    fn default() -> RPSPlayer {
        RPSPlayer {
            win_score: 6,
            draw_score: 3,
            lose_score: 0,

            rock_score: 1,
            paper_score: 2,
            scissors_score: 3,

            wins: vec![vec!["A".to_string(), "C".to_string()],
                       vec!["B".to_string(), "A".to_string()],
                       vec!["C".to_string(), "B".to_string()]],
            draws: vec![vec!["A".to_string(), "A".to_string()],
                        vec!["B".to_string(), "B".to_string()],
                        vec!["C".to_string(), "C".to_string()]],
            losses: vec![vec!["C".to_string(), "A".to_string()],
                         vec!["A".to_string(), "B".to_string()],
                         vec!["B".to_string(), "C".to_string()]],
        }
    }

    fn evaluate(&self, player_move: &str, opponent_move: &str) -> usize {
        let player_move = RPSPlayer::translate_move(player_move);
        let opponent_move = RPSPlayer::translate_move(opponent_move);
        let mut score = self.get_move_score(player_move);

        let move_vector = vec![player_move.to_string(), opponent_move.to_string()];
        if self.wins.contains(&move_vector) { score += self.win_score }
        else if self.draws.contains(&move_vector) { score += self.draw_score }
        else if self.losses.contains(&move_vector) { score += self.lose_score }
        else { panic!("Incorrect move vector: ({}, {})", move_vector[0], move_vector[1]) }

        return score;
    }

    fn evaluate_with_result(&self, result: &str, opponent_move: &str) -> usize {
        let mut move_to_play: &str = "";

        if result == "X" {
            for loss in &self.losses {
                if loss[1] == opponent_move {
                    move_to_play = &*loss[0];
                    break
                }
            }
        }
        else if result == "Y" {
            for draw in &self.draws {
                if draw[1] == opponent_move {
                    move_to_play = &draw[0];
                    break
                }
            }
        }
        else if result == "Z" {
            for win in &self.wins {
                if win[1] == opponent_move {
                    move_to_play = &win[0];
                    break
                }
            }
        }

        return self.evaluate(move_to_play, opponent_move);
    }

    fn translate_move(played_move: &str) -> &str {
        if played_move == "X" || played_move == "A" { return "A" };
        if played_move == "Y" || played_move == "B" { return "B" };
        if played_move == "Z" || played_move == "C" { return "C" };
        panic!("Invalid move: {}", played_move);
    }

    fn get_move_score(&self, played_move: &str) -> usize {
        if played_move == "A" { return self.rock_score };
        if played_move == "B" { return self.paper_score };
        if played_move == "C" { return self.scissors_score };
        panic!("Invalid move: {}", played_move);
    }
}


fn main() {
    let watch = Stopwatch::start_new();

    let file = File::open("../inputs/2022/day2.txt").unwrap();
    let reader = BufReader::new(file);
    let mut data: Vec<String> = vec![];

    for line in reader.lines() {
        data.push(line.unwrap());
    }
    let file_read_time = watch.us();

    // part 1
    let mut total_score = 0;
    let game = RPSPlayer::default();
    for moves in &data {
        let split_moves: Vec<&str> = moves.split(" ").collect();
        total_score += game.evaluate(split_moves[1], split_moves[0]);
    }
    let part1_time = watch.us() - file_read_time;
    println!("{}", total_score);

    // part 2
    total_score = 0;
    for moves in &data {
        let split_moves: Vec<&str> = moves.split(" ").collect();
        total_score += game.evaluate_with_result(split_moves[1], split_moves[0]);
    }
    let part2_time = watch.us() - part1_time - file_read_time;
    println!("{}", total_score);

    println!();
    println!("Total time: {:.0} microseconds.", watch.us());
    println!("File read time: {:.0} microseconds.", file_read_time);
    println!("Execution time: {:.0} microseconds.", part1_time + part2_time);
    println!();
    println!("Part 1 execution time: {:.0} microseconds.", part1_time);
    println!("Part 2 execution time: {:.0} microseconds.", part2_time);
}
