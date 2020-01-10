import React from 'react';
import './command.scss';

const axios = require('axios');

class Command extends React.Component {

  backendUrl = null;

  constructor() {
    super();
    this.backendUrl = 'http://localhost:8080/';
  }

  setFocus() {
    setTimeout(() => {
      document.getElementsByClassName('cmd')[0].focus();
    }, 5);
  }

  sendToBackend(command) {
    const data = {'command': command};
    const headers = {headers: {'Access-Control-Allow-Origin': '*'}};
    return axios.post(this.backendUrl + 'execute', data, headers)
      .then(response => {
        if (response.data['response'] === 'BAD COMMAND') {
            return command + ': command not found'
        }
        return response.data['response'];
      })
      .catch(error => {
        return 'BACKEND FAILURE! ' + error;
      });
  }

  execute(e) {
    if (e.key === 'Enter') {
      const command = e.currentTarget.value;
      const inputs = document.getElementsByClassName('cmd');
      const input = inputs[inputs.length - 1];
      const span = input.parentNode;

      span.removeChild(input);
      span.innerHTML += command;


      this.sendToBackend(command).then(message => {
        this.props.onEnter(message);
      });
    }
  }

  render() {

    let handle = '>>> ';
    if (this.props.username !== null && this.props.username !== undefined) {
      handle = this.props.username + ' ' + handle;
    }
    return (
      <span>{handle}
        <input
          className='cmd'
          onBlur={this.setFocus}
          onKeyDown={this.execute.bind(this)}
          type='text'
          autoFocus>
        </input>
      </span>
    );
  }
}

export default Command;
