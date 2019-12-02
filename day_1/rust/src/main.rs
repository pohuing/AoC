#![feature(test)]
extern crate test;
use std::fs;
use std::io::{prelude::*, BufReader};
use std::collections::HashMap;


fn main() {
    let modules = read_file();
    println!("Part one: {}", day_one_part_one(&modules));
    println!("Part two: {}", day_one_part_two(&modules));
}

fn read_file() -> Vec<u64> {
    let file = fs::File::open("../input.txt").expect("Failed to read file");
    BufReader::new(file)
        .lines()
        .map(|line| line.unwrap().parse().unwrap())
        .collect()
}


fn day_one_part_one(modules: &Vec<u64>) -> u64 {
    modules.iter().map(|&x| direct_fuel(x)).sum::<u64>()
}

fn day_one_part_two(modules: &Vec<u64>) -> u64 {
    modules.iter().map(|&x| indirect_fuel(x)).sum::<u64>()
}

fn day_one_part_two_memoized(modules: &Vec<u64>) -> u64 {
    let mut lookup_table = setup_lookup_table();
    modules.iter().map(|&x| indirect_fuel_memoized(x, &mut lookup_table)).sum::<u64>()
}

fn setup_lookup_table() -> HashMap<u64, u64>{
    let mut lookup_table = HashMap::new();
    lookup_table.insert(0, 0);
    lookup_table.insert(1, 0);
    lookup_table.insert(2, 0);
    lookup_table.insert(3, 1);
    lookup_table
}

fn direct_fuel(weight: u64) -> u64 {
    let weight = weight / 3;
    if weight < 3 {
        0
    }else{
        weight - 2
    }
}

fn indirect_fuel(weight: u64) -> u64{
    let required_fuel = direct_fuel(weight);
    if required_fuel > 2 {
        required_fuel + indirect_fuel(required_fuel)
    }else{
        required_fuel
    }
}

fn indirect_fuel_memoized(weight: u64, lookup_table: &mut HashMap<u64, u64>) -> u64{
    match lookup_table.get(&weight).map(|n| n.clone()){
        Some(n) => n,
        None => {
            let direct_cost = direct_fuel(weight);
            let total_cost = direct_cost + indirect_fuel_memoized(direct_cost, lookup_table);
            lookup_table.insert(weight, total_cost);
            total_cost
        }
    }
}

#[cfg(test)]
mod tests{
use super::*;
use test::Bencher;


    #[test]
    fn direct_fuel_test(){
        assert_eq!(2, direct_fuel(12));
        assert_eq!(2, direct_fuel(14));
        assert_eq!(654, direct_fuel(1969));
        assert_eq!(33583, direct_fuel(100756));
    }

    #[test]
    fn day_one_part_one_test(){
        let modules = read_file();
        assert_eq!(3273471, day_one_part_one(&modules))
    }

    #[bench]
    fn day_one_part_one_bench(b: &mut Bencher){
        let modules = read_file();
        b.iter(|| day_one_part_one(&modules))
    }

    #[test]
    fn indirect_fuel_test() {
        assert_eq!(2, indirect_fuel(12));
        assert_eq!(2, indirect_fuel(14));
        assert_eq!(966, indirect_fuel(1969));
        assert_eq!(50346, indirect_fuel(100756));
    }
    
    #[test]
    fn day_one_part_two_test() {
        let modules = read_file();
        assert_eq!(4907345, day_one_part_two(&modules));
    }
    
    #[bench]
    fn day_one_part_two_bench(b: &mut Bencher){
        let modules = read_file();
        b.iter(|| day_one_part_two(&modules))
    }

    #[test]
    fn indirect_fuel_memoized_test() {
        let mut lookup_table = setup_lookup_table();
        assert_eq!(2, indirect_fuel_memoized(12, &mut lookup_table));
        let mut lookup_table = setup_lookup_table();
        assert_eq!(2, indirect_fuel_memoized(14, &mut lookup_table));
        let mut lookup_table = setup_lookup_table();
        assert_eq!(966, indirect_fuel_memoized(1969, &mut lookup_table));
        let mut lookup_table = setup_lookup_table();
        assert_eq!(50346, indirect_fuel_memoized(100756, &mut lookup_table));
    }

    #[test]
    fn day_one_part_two_memoized_test() {
        let modules = read_file();
        assert_eq!(4907345, day_one_part_two_memoized(&modules));
    }

    #[bench]
    fn day_one_part_two_memoized_bench(b: &mut Bencher){
        let modules = read_file();
        b.iter(|| day_one_part_two_memoized(&modules))
    }
}
