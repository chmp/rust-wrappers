use std::{ffi::CStr, mem, os::raw::c_char, slice};

use rust_core::Params;

#[no_mangle]
pub fn params_new() -> Box<Params> {
    Box::new(Params::new())
}

#[no_mangle]
pub fn params_free(params: Box<Params>) {
    mem::drop(params);
}

#[no_mangle]
pub fn params_insert(
    params: &mut Params,
    name: *const c_char,
    data_ptr: *const u8,
    data_len: u64,
) -> u8 {
    let name = unsafe { CStr::from_ptr(name) };
    let data = unsafe { slice::from_raw_parts(data_ptr, data_len as usize) };

    let name = match name.to_str() {
        Ok(name) => name,
        Err(_) => return 1,
    };

    params.insert(name.to_owned(), data.to_owned());

    0
}

#[no_mangle]
pub fn params_len(params: &Params) -> u64 {
    params.len() as u64
}
