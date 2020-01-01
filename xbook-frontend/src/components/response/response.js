import React from 'react';
import './response.scss';

class Response extends React.Component {
  render() {
    return (
      <p>{this.props.mess}</p>
    );
  }
}

export default Response;
