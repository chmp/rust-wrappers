use wasm_bindgen::prelude::*;

use rust_core::Params as CoreParams;

#[wasm_bindgen]
pub struct Params {
    params: CoreParams,
}

#[wasm_bindgen]
impl Params {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Params {
        Params {
            params: CoreParams::new(),
        }
    }

    pub fn len(&self) -> usize {
        self.params.len()
    }

    pub fn set(&mut self, key: String, data: Vec<u8>) {
        self.params.insert(key, data);
    }

    pub fn get(&self, key: &str) -> Option<Vec<u8>> {
        self.params.get(key).map(|v| v.to_owned())
    }
}

#[wasm_bindgen]
pub fn add(a: u32, b: u32) -> u32 {
    a + b
}
