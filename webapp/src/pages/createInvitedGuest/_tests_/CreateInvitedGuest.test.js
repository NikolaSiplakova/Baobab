import React from 'react';
import { shallow } from 'enzyme';
import CreateInvitedGuest from './../components/CreateInvitedGuest';

test('Check if CreateInvitedGuest renders.', () => {
  // Render Application Form Page.
  const wrapper = shallow(<CreateInvitedGuest />);
  expect(wrapper.length).toEqual(1);
});