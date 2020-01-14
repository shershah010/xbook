import React from 'react';
import './response.scss';

class Response extends React.Component {
  render() {
    return (
      <div>
        <pre>{this.props.mess}</pre>
      </div>
    );
  }
}

export default Response;
