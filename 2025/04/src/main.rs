use std::fs::File;
use std::io::prelude::*;

fn main() {
    part1();
    part2();
}

fn part1() {
    let file_content = get_text("input.txt");
    let grid = to_grid(&file_content);
    let mut sum = 0;
    let size = (grid.len(), grid[0].len());
    for x in 0..size.0 {
        for y in 0..size.1 {
            if grid[x][y] == 1 && count_neighbors(&grid, x, y, size.0, size.1) < 4 {
                sum += 1;
            }
        }
    }
    println!("{}", sum);
}

fn part2() {
    let file_content = get_text("input.txt");
    let mut grid = to_grid(&file_content);
    let mut sum = 0;
    let size = (grid.len(), grid[0].len());

    loop {
        let mut found = false;

        for x in 0..grid.len() {
            for y in 0..grid[0].len() {
                if grid[x][y] == 1 && count_neighbors(&grid, x, y, size.0, size.1) < 4 {
                    sum += 1;

                    grid[x][y] = 0;
                    found = true;
                }
            }
        }

        if !found {
            break;
        }
    }
    println!("{}", sum);
}

fn to_grid(content: &str) -> Vec<Vec<u32>> {
    content
        .lines()
        .map(|l| {
            l.chars()
                .map(|c| match c {
                    '@' => 1,
                    _ => 0,
                })
                .collect()
        })
        .collect()
}

fn count_neighbors(
    matrix: &Vec<Vec<u32>>,
    x: usize,
    y: usize,
    row_count: usize,
    col_count: usize,
) -> u32 {
    let offsets = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ];
    let mut count = 0;
    for &(dx, dy) in &offsets {
        let new_x = x as isize + dx;
        let new_y = y as isize + dy;
        if is_within_bounds(new_x, new_y, row_count, col_count) {
            count += matrix[new_x as usize][new_y as usize];
        }
    }
    count
}

fn is_within_bounds(x: isize, y: isize, row_count: usize, col_count: usize) -> bool {
    x >= 0 && x < row_count as isize && y >= 0 && y < col_count as isize
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
    fn test_to_grid() {
        let input = "..@
@..
.@@";
        let grid = to_grid(input);
        let expected = vec![vec![0, 0, 1], vec![1, 0, 0], vec![0, 1, 1]];
        assert_eq!(grid, expected);
    }

    #[test]
    fn test_count_adjacent() {
        let mat = vec![vec![0, 0, 1], vec![1, 0, 0], vec![0, 1, 1]];
        assert_eq!(count_neighbors(&mat, 0, 0, 3, 3), 1);
        assert_eq!(count_neighbors(&mat, 0, 1, 3, 3), 2);
        assert_eq!(count_neighbors(&mat, 1, 1, 3, 3), 4);
    }
}
