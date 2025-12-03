use std::fs::File;
use std::io::prelude::*;

fn main() {
    part1();
}

fn part1() {
    let file_content = get_text("input.txt");
    let lines = to_lines(&file_content);
    let sum = lines.iter().map(get_line_value).sum::<u32>();
    println!("{}", sum);
}

fn to_lines(content: &str) -> Vec<Vec<u32>> {
    content
        .lines()
        .map(|l| l.chars().filter_map(|char| char.to_digit(10)).collect())
        .collect()
}

fn get_line_value(line: &Vec<u32>) -> u32 {
    let mut first_idx = 0;
    for i in 1..line.len() - 1 {
        if line[i] > line[first_idx] {
            first_idx = i;
        }
    }
    let mut second_idx = first_idx + 1;
    for i in first_idx + 1..line.len() {
        if line[i] > line[second_idx] {
            second_idx = i;
        }
    }
    line[first_idx] * 10 + line[second_idx]
}

fn get_text(filename: &str) -> String {
    let mut file = File::open(filename).expect("cannot open input.txt file");
    let mut contents = String::new();
    file.read_to_string(&mut contents)
        .expect("cannot read string from file");
    contents
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_to_lines() {
        let content = "1234
5678
1111";
        let expected = vec![vec![1, 2, 3, 4], vec![5, 6, 7, 8], vec![1, 1, 1, 1]];
        assert_eq!(to_lines(content), expected);
    }

    #[test]
    fn test_line_value() {
        assert_eq!(get_line_value(&vec![1, 2, 3, 4, 5]), 45);
        assert_eq!(get_line_value(&vec![9, 8, 7, 6]), 98);
        assert_eq!(
            get_line_value(&vec![9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1]),
            98
        );
        assert_eq!(
            get_line_value(&vec![8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9]),
            89
        );
        assert_eq!(
            get_line_value(&vec![2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 7, 8]),
            78
        );
        assert_eq!(
            get_line_value(&vec![8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 2, 1, 1, 1, 1]),
            92
        );
    }
}
