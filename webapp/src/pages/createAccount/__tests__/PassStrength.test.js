import React from 'react';
import { shallow } from 'enzyme';
import PassStrength from './../components/PassStrength';

test('Check if PassStrength renders.', () => {
  // Render Application Form Page.
  const wrapper = shallow(<PassStrength />);
  expect(wrapper.length).toEqual(1);
});