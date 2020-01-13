import React from 'react';
import './command.scss';

const axios = require('axios');

class Command extends React.Component {

  backendUrl = null;
  handle = null;

  constructor(props) {
    super(props);
    this.backendUrl = 'http://localhost:8080/';
    this.handle = '>>> ';
    if (this.props.username !== null && this.props.username !== undefined) {
      this.handle = this.props.username + ' ' + this.handle;
    }
  }

  sendToBackend(command) {
    const data = {
      'command': command,
      'token': this.props.token
    };
    const headers = {headers: {'Access-Control-Allow-Origin': '*'}};
    return axios.post(this.backendUrl + 'execute', data, headers)
      .then(response => {
        return response.data;
      })
      .catch(error => {
        console.log(error);
        return {'response': 'BACKEND FAILURE! ' + error};
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

      if (command === 'login') {
        this.props.onEnter('login', this.handle);
        return;
      }

      this.sendToBackend(command).then(message => {
        if (message['response'] === 'BAD COMMAND') {
          this.props.onEnter(command + ': command not found');
        } else {
          this.props.onEnter(message['response']);
        }
      });
    }
  }

  render() {
    return (
      <div>
        <span>{this.handle}
          <input
            className='cmd'
            onKeyDown={this.execute.bind(this)}
            type='text'
            autoFocus>
          </input>
      </span>
    </div>
    );
  }
}

export default Command;
