import React from 'react';
import { render } from '@testing-library/react';
import Response from './response';

test('renders message', () => {
  const { getByText } = render(<Response mess="a message"></Response>);
  const mess = getByText(/a message/i);
  expect(mess).toBeInTheDocument();
});
