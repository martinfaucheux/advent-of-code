use std::fs::File;
use std::io::prelude::*;

fn main() {
    part1();
    part2();
}

enum Direction {
    Left,
    Right,
}

struct Rotation {
    dir: Direction,
    degrees: u32,
}

fn extract_rotations(text: &str) -> Vec<Rotation> {
    let mut rotations: Vec<Rotation> = vec![];

    for line in text.lines() {
        let (dir_char, deg_str) = line.split_at(1);
        let dir = match dir_char {
            "L" => Direction::Left,
            "R" => Direction::Right,
            _ => panic!("invalid direction"),
        };
        let degrees = deg_str.parse::<u32>().expect("invalid degrees");
        rotations.push(Rotation { dir, degrees });
    }

    rotations
}

fn part1() {
    let file_content = get_text("input.example.txt");
    let rotations = extract_rotations(&file_content);

    let mut counter: u32 = 0;
    let mut position: u32 = 50;
    for rotation in rotations {
        let disp = match rotation.dir {
            Direction::Left => -1,
            Direction::Right => 1,
        } * rotation.degrees as i32;
        position = (position as i32 + disp).rem_euclid(100) as u32;

        if position == 0 {
            counter += 1;
        }
    }

    println!("{}", counter);
}

fn part2() {
    let file_content = get_text("input.txt");
    let rotations = extract_rotations(&file_content);

    let mut counter: u32 = 0;
    let mut position: i32 = 50;
    println!("The dial starts by pointing at 50");
    for rotation in rotations {
        let disp = match rotation.dir {
            Direction::Left => -1,
            Direction::Right => 1,
        };

        for _ in 0..rotation.degrees {
            position += disp;
            if position % 100 == 0 {
                counter += 1;
            }
        }
        position = position.rem_euclid(100);
    }

    println!("{}", counter);
}

fn get_text(filename: &str) -> String {
    let mut file = File::open(filename).expect("cannot open input.txt file");
    let mut contents = String::new();
    file.read_to_string(&mut contents)
        .expect("cannot read string from file");
    contents
}
