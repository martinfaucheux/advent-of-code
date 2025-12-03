use std::fs::File;
use std::io::prelude::*;

fn main() {
    part1();
    part2();
}

fn part1() {
    let file_content = get_text("input.txt");
    let lines = to_lines(&file_content);
    let sum = lines
        .iter()
        .map(|line| get_line_value(line, 2))
        .sum::<u64>();
    println!("{}", sum);
}

fn part2() {
    let file_content = get_text("input.txt");
    let lines = to_lines(&file_content);
    let sum = lines
        .iter()
        .map(|line| get_line_value(line, 12))
        .sum::<u64>();
    println!("{}", sum);
}

fn to_lines(content: &str) -> Vec<Vec<u64>> {
    content
        .lines()
        .map(|l| {
            l.chars()
                .filter_map(|char| char.to_digit(10).map(|d| d as u64))
                .collect()
        })
        .collect()
}

fn get_line_value(line: &Vec<u64>, value_count: usize) -> u64 {
    let mut indices: Vec<usize> = vec![];
    let mut start_idx = 0;
    let line_length = line.len();
    for i in 0..value_count {
        // il faut caller (value_count - i) depuis la fin
        let last_idx = line_length - (value_count - i - 1);
        let max_idx = start_idx + get_biggest_idx(&line[start_idx..last_idx]);
        indices.push(max_idx);
        start_idx = max_idx + 1;
    }

    build_number(&indices.iter().map(|idx| line[*idx]).collect::<Vec<u64>>())
}

fn build_number(numbers: &Vec<u64>) -> u64 {
    let value_count = numbers.len();
    numbers
        .iter()
        .enumerate()
        .map(|(i, &val)| {
            let power = (value_count - i - 1) as u32;
            val * 10u64.pow(power)
        })
        .sum::<u64>()
}

fn get_biggest_idx(line: &[u64]) -> usize {
    let mut biggest_idx = 0;
    for i in 1..line.len() {
        if line[i] > line[biggest_idx] {
            biggest_idx = i;
        }
    }
    biggest_idx
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
    fn test_build_number() {
        assert_eq!(build_number(&vec![1, 2, 3, 4, 5]), 12345);
        assert_eq!(build_number(&vec![9, 8, 7, 6]), 9876);
        assert_eq!(build_number(&vec![0, 0, 1]), 1);
    }

    #[test]
    fn test_line_value_2() {
        assert_eq!(get_line_value(&vec![2, 1], 2), 21);
        assert_eq!(get_line_value(&vec![1, 2], 2), 12);
        assert_eq!(get_line_value(&vec![1, 2, 3, 4, 5], 2), 45);
        assert_eq!(get_line_value(&vec![9, 8, 7, 6], 2), 98);
        assert_eq!(
            get_line_value(&vec![9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1], 2),
            98
        );
        assert_eq!(
            get_line_value(&vec![8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9], 2),
            89
        );
        assert_eq!(
            get_line_value(&vec![2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 7, 8], 2),
            78
        );
        assert_eq!(
            get_line_value(&vec![8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 2, 1, 1, 1, 1], 2),
            92
        );
    }

    #[test]
    fn test_line_value_12() {
        assert_eq!(
            get_line_value(&vec![9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1], 12),
            987654321111
        );
        assert_eq!(
            get_line_value(&vec![8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9], 12),
            811111111119
        );
        assert_eq!(
            get_line_value(
                &vec![
                    // 234234234234278
                    2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 7, 8
                ],
                12
            ),
            434234234278
        );
        assert_eq!(
            get_line_value(
                &vec![
                    // 818181911112111
                    8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 1, 2, 1, 1, 1
                ],
                12
            ),
            888911112111
        );
    }
}
