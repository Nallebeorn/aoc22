fn get_input() -> Vec<i32> {
    include_str!("input.txt")
        .lines()
        .map(|num_as_str| match num_as_str.parse() {
            Ok(num) => num,
            Err(err) => {
                panic!("Couldn't parse '{num_as_str}' due to {err}");
            }
        })
        .collect()
}

pub fn run() {
    println!("\n**** DAY 00 part 1 ****");
    run1();
    println!("\n**** DAY 00 part 2 ****");
    run2();
}

pub fn run1() {
    let input = get_input();

    let mut num_increases = 0;

    for i in 1..input.len() {
        let previous = input[i - 1];
        let current = input[i];

        if current > previous {
            num_increases += 1;
        }
    }

    println!("Depth measurement increased a total of {num_increases} times");
}

pub fn run2() {
    let sliding_window_size = 3;

    let input = get_input();

    let mut num_increases = 0;

    let mut sliding_windows: Vec<Vec<i32>> = Vec::new();

    for depth_index in 0..input.len() {
        sliding_windows.push(Vec::new());

        let depth = input[depth_index];

        let mut prev_window: Option<&Vec<i32>> = None;
        for window in &mut sliding_windows {
            if window.len() < sliding_window_size {
                window.push(depth);
                if window.len() >= sliding_window_size {
                    let curr_sum: i32 = window.iter().sum();
                    print!("Sum: {curr_sum} ");
                    if let Some(prev_window) = prev_window {
                        let prev_sum: i32 = prev_window.iter().sum();
                        if curr_sum > prev_sum {
                            num_increases += 1;
                            println!("(increased!)")
                        } else {
                            println!("(no increase)");
                        }
                    }
                }
            }

            prev_window = Some(window);
        }
    }

    println!("Depth measurement in sliding window increased from previous window a total of {num_increases} times");
}
