use pyo3::{buffer::PyBuffer, exceptions, prelude::*, types::PyBytes};

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

    fn __len__(&self) -> usize {
        self.params.len()
    }

    fn __setitem__(&mut self, py: Python, name: String, data: PyBuffer<u8>) -> PyResult<()> {
        self.params.insert(name, data.to_vec(py)?);
        Ok(())
    }

    fn __getitem__(&self, py: Python, name: &str) -> PyResult<PyObject> {
        let param = match self.params.get(name) {
            Some(param) => param,
            None => {
                return Err(PyErr::new::<exceptions::PyKeyError, _>(format!(
                    "Could not find {}",
                    name
                )))
            }
        };

        let param = PyBytes::new(py, param).to_object(py);
        Ok(param)
    }
}

#[pymodule]
fn pyo3_wrapper(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Params>()?;
    Ok(())
}
