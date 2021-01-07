import React from 'react';
import { shallow } from 'enzyme';
import Address from './../components/Address';

test('Check if Address renders.', () => {
  // Render Application Form Page.
  const wrapper = shallow(<Address />);
  expect(wrapper.length).toEqual(1);
});