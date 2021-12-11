use pyo3::{buffer::PyBuffer, prelude::*};

use rust_core::Params as CoreParams;

#[pyclass]
struct Params {
    params: CoreParams,
}

#[pymethods]
impl Params {
    #[new]
    fn new() -> Self {
        Params {
            params: Default::default(),
        }
    }

    fn __setitem__(&mut self, py: Python, name: String, data: PyBuffer<u8>) -> PyResult<()> {
        self.params.insert(name, data.to_vec(py)?);
        Ok(())
    }
}

#[pymodule]
fn pyo3_wrapper(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Params>()?;
    Ok(())
}
