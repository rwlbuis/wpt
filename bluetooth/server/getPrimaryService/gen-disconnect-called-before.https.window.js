// META: script=/resources/testharness.js
// META: script=/resources/testharnessreport.js
// META: script=/resources/testdriver.js
// META: script=/resources/testdriver-vendor.js
// META: script=/bluetooth/resources/bluetooth-helpers.js
// Generated by //third_party/WebKit/LayoutTests/bluetooth/generate.py
'use strict';
const test_desc = 'disconnect() called before getPrimaryService. ' +
    'Reject with NetworkError.';
const expected = new DOMException(
    'GATT Server is disconnected. Cannot retrieve services. (Re)connect ' +
        'first with `device.gatt.connect`.',
    'NetworkError');
let device;

bluetooth_test(
    () => getConnectedHealthThermometerDevice({
            filters: [{services: ['health_thermometer']}],
            optionalServices: ['generic_access']
          })
              .then(_ => ({device} = _))
              .then(() => device.gatt.disconnect())
              .then(
                  () => assert_promise_rejects_with_message(
                      device.gatt.getPrimaryService('health_thermometer'),
                      expected)),
    test_desc);
