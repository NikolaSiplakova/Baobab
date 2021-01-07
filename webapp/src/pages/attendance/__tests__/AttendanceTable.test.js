import React from 'react';
import { shallow } from 'enzyme';
import AttendanceTable from './../components/AttendanceTable';

test('Check if AttendanceTable renders.', () => {
  // Render Application Form Page.
  const wrapper = shallow(<AttendanceTable />);
  expect(wrapper.length).toEqual(1);
});