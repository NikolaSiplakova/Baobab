import React from 'react';
import { shallow } from 'enzyme';
import CreateAccountForm from './../components/CreateAccountForm';

// Mock Props
const props = {
    loggedIn: "John",
    organisation: "Google",
}

test('Check if CreateAccountForm renders with mocked data.', () => {
  // Render Application Form Page.
  const wrapper = shallow(<CreateAccountForm {...props}/>);
  expect(wrapper.length).toEqual(1);
});

test("Was Data call is successful.", async () => {
    const wrapper = shallow(<ResponsePage {...props} />);
    await wrapper.instance().fetchData();
    expect(wrapper.state().applicationData.id).toBeTruthy();
});