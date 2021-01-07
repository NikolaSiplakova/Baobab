import React from 'react';
import { shallow } from 'enzyme';
import ApplicationForm from './../components/ApplicationForm';

test('Check if ApplicationForm renders.', () => {
  // Render Application Form Page.
  const wrapper = shallow(<ApplicationForm />);
  expect(wrapper.length).toEqual(1);
});