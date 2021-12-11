#![allow(unused_unsafe)]
use std::{ffi::CStr, mem, os::raw::c_char, ptr, slice};

use rust_core::Params;

#[no_mangle]
pub fn params_new() -> Box<Params> {
    Box::new(Params::new())
}

#[no_mangle]
pub fn params_free(params: Box<Params>) {
    mem::drop(params);
}

/// Insert a parameter into the collection
///
/// # Safety
///
/// `name` must be a valid NULL-terminated UTF8-encoded string and `data` must
/// not alias any memory region owned by `params`.
///
#[no_mangle]
pub unsafe fn params_insert(
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

/// Get the length of a parameter
///
/// If an error is encountered or the parameter cannot be found, -1 is returned.
///
/// # Safety
///
/// `name` must be a valid NULL-terminated UTF8-encoded string.
///
#[no_mangle]
pub unsafe fn params_param_len(params: &Params, name: *const c_char) -> i64 {
    let name = unsafe { CStr::from_ptr(name) };
    let name = match name.to_str() {
        Ok(name) => name,
        Err(_) => return -1,
    };

    params.get(name).map(|d| d.len() as i64).unwrap_or(-1)
}

/// Get the data of a parameter
///
/// If an error is encountered or the parameter cannot be found, null is
/// returned.
///
/// # Safety
///
/// `name` must be a valid NULL-terminated UTF8-encoded string. The `params`
/// objects must not be modified, while the returned pointer is used.
///
#[no_mangle]
pub unsafe fn params_param_data(params: &Params, name: *const c_char) -> *const u8 {
    let name = unsafe { CStr::from_ptr(name) };
    let name = match name.to_str() {
        Ok(name) => name,
        Err(_) => return ptr::null(),
    };

    params
        .get(name)
        .map(|d| d.as_ptr())
        .unwrap_or_else(ptr::null)
}

#[no_mangle]
pub fn params_len(params: &Params) -> u64 {
    params.len() as u64
}
