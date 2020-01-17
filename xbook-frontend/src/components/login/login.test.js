import React from 'react';
import { render } from '@testing-library/react';
import Login from './login';

function dummyFunction(a, b) { }

test('renders login', () => {
  const { getByText } = render(<Login token={"not null"} onEnter={dummyFunction}></Login>);
  const mess = getByText(/username/i);
  expect(mess).toBeInTheDocument();
});
