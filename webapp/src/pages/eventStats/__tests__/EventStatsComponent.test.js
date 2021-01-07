import React from 'react';
import { shallow } from 'enzyme';
import EventStatsComponent from './../components/EventStatsComponent';

test('Check if EventStatsComponent renders.', () => {
  // Render Application Form Page.
  const wrapper = shallow(<EventStatsComponent />);
  expect(wrapper.length).toEqual(1);
});