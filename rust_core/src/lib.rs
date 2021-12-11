mod util;

#[cfg(test)]
mod test;

use std::collections::HashMap;

ignore! {

pub struct Params {
    /* ... */
}

impl Params {
    pub fn new() -> Self {
        /* ... */
    }

    pub fn insert(&mut self, name: String, data: Vec<u8>) {
        /* ... */
    }
}

}

#[derive(Default, Clone)]
pub struct Params {
    params: HashMap<String, Vec<u8>>,
    names: Vec<String>,
}

impl Params {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn insert(&mut self, name: String, data: Vec<u8>) {
        if !self.params.contains_key(&name) {
            self.names.push(name.to_owned());
        }
        self.params.insert(name, data);
    }
}
