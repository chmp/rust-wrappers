use std::collections::HashMap;

use base64::DecodeError;
use serde::{Deserialize, Serialize};

#[derive(Default, Clone, Deserialize)]
#[serde(try_from = "SerDeParams", into = "SerDeParams")]
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

    pub fn get(&self, name: &str) -> Option<&[u8]> {
        self.params.get(name).map(|v| v.as_slice())
    }

    pub fn len(&self) -> usize {
        self.params.len()
    }

    pub fn is_empty(&self) -> bool {
        self.params.is_empty()
    }
}

#[derive(Clone, Debug, Default, Serialize, Deserialize)]
struct SerDeParams {
    params: HashMap<String, String>,
}

impl TryFrom<SerDeParams> for Params {
    type Error = DecodeError;

    fn try_from(value: SerDeParams) -> Result<Params, DecodeError> {
        let mut res = Params::new();

        for (key, value) in value.params {
            res.insert(key, base64::decode(value)?);
        }

        Ok(res)
    }
}

impl From<Params> for SerDeParams {
    fn from(value: Params) -> Self {
        let mut res = SerDeParams {
            params: Default::default(),
        };

        for (key, value) in value.params {
            res.params.insert(key, base64::encode(value));
        }

        res
    }
}

#[cfg(test)]
mod test;
