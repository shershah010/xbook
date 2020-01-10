import React from 'react';
import './response.scss';

class Response extends React.Component {
  render() {
    return (
      <pre>{this.props.mess}</pre>
    );
  }
}

export default Response;
