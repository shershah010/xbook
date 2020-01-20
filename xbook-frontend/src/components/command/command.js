import React from 'react';
import './command.scss';

const axios = require('axios');

class Command extends React.Component {

  backendUrl = null;
  handle = null;
  specialCMDs = null;
  index = -1;

  constructor(props) {
    super(props);
    this.backendUrl = 'https://xbook010.appspot.com/';
    this.handle = '>>> ';
    if (this.props.username !== null && this.props.username !== undefined) {
      this.handle = this.props.username + ' ' + this.handle;
    }
    this.specialCMDs = ['login', 'register'];
    this.index = this.props.commands.length;
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

  execute(value) {
    const command = value;
    const inputs = document.getElementsByClassName('cmd');
    const input = inputs[inputs.length - 1];
    const span = input.parentNode;

    span.removeChild(input);
    span.innerHTML += command;

    if (this.specialCMDs.includes(command)) {
      this.props.onEnter(command, command);
      return;
    }

    if (this.props.token === null) {
      this.props.onEnter(command, 'Permission denied');
      return;
    }

    this.sendToBackend(command).then(message => {
      if (message['response'] === 'BAD COMMAND') {
        this.props.onEnter(command, command + ': command not found');
      } else {
        this.props.onEnter(command, message['response']);
      }
    });
  }

  handleKeyPress(e) {
    if (e.key === 'Enter') {
      this.execute(e.currentTarget.value);
    } else if (e.key === 'ArrowUp') {
      if (this.index > 0) {
        this.index -= 1;
        e.currentTarget.value = this.props.commands[this.index];
      }
    } else if (e.key === 'ArrowDown') {
      if (this.index < this.props.commands.length) {
        this.index += 1;
        const val = this.props.commands[this.index];
        e.currentTarget.value = val ? val : '';
      }
    } else if (e.ctrlKey && e.key === 'c') {
      this.props.onEnter(e.currentTarget.value, '');
      return;
    }
  }

  render() {
    return (
      <div>
        <span>{this.handle}
          <input
            className='cmd'
            onKeyDown={this.handleKeyPress.bind(this)}
            type='text'
            autoFocus>
          </input>
      </span>
    </div>
    );
  }
}

export default Command;
