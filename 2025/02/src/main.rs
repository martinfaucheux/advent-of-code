use std::fs::File;
use std::io::prelude::*;

fn main() {
    part1();
}

fn part1() {
    let file_content = get_text("input.txt");
    let tuples = get_tuples(&file_content);

    let mut count: u64 = 0;
    for (start, end) in tuples {
        for n in start..(end + 1) {
            if is_repeating(n) {
                count += n;
            }
        }
    }

    println!("{}", count);
}

fn is_repeating(n: u64) -> bool {
    if n < 11 {
        return false;
    }
    let str_n = n.to_string();
    for i in 1..(str_n.chars().count()) {
        if str_n[..i] == str_n[i..] {
            return true;
        }
    }

    return false;
}

fn get_tuples(text: &str) -> Vec<(u64, u64)> {
    text.split(",")
        .filter_map(|s| {
            let mut split = s.split("-");
            match (split.next(), split.next()) {
                (Some(first), Some(second)) => Some((
                    first.parse::<u64>().unwrap(),
                    second.parse::<u64>().unwrap(),
                )),
                _ => None,
            }
        })
        .collect()
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
    fn test_is_repeating() {
        // true
        assert_eq!(is_repeating(99), true);
        assert_eq!(is_repeating(1010), true);
        assert_eq!(is_repeating(1188511885), true);
        assert_eq!(is_repeating(222222), true);
        assert_eq!(is_repeating(38593859), true);
        // false
        assert_eq!(is_repeating(1), false);
        assert_eq!(is_repeating(101), false);
        assert_eq!(is_repeating(3330333), false);
    }

    #[test]
    fn test_get_tuples() {
        // true
        let input_str = "10-20,30-40,50-60";
        assert_eq!(get_tuples(input_str), vec![(10, 20), (30, 40), (50, 60)]);
    }
}
