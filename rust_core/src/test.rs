use super::Params;

#[test]
fn example() {
    let mut params = Params::new();
    params.insert(String::from("foo"), vec![0, 1, 2]);
}
