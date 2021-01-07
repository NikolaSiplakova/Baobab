import React from 'react';
import { shallow } from 'enzyme';
import ReferenceRequestRowComponent from './../components/ReferenceRequest';

test('Check if ReferenceRequestRow renders.', () => {
  // Render Application Form Page.
  const wrapper = shallow(<ReferenceRequestRowComponent />);
  expect(wrapper.length).toEqual(1);
});


