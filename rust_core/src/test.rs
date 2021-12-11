use super::Params;

#[test]
fn example() {
    let mut params = Params::new();
    assert_eq!(params.len(), 0);

    params.insert(String::from("foo"), vec![0, 1, 2]);
    assert_eq!(params.len(), 1);

    assert_eq!(params.get("foo").unwrap(), &[0, 1, 2]);
}
