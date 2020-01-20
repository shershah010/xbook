import React from 'react';
import './login.scss';

const axios = require('axios');

class Login extends React.Component {

  username = null;
  backendUrl = null;

  constructor() {
    super();
    this.backendUrl = 'https://xbook010.appspot.com/';
  }

  setFocus() {
    setTimeout(() => {
      document.getElementsByClassName('cmd')[0].focus();
    }, 5);
  }

  backendLogin(password) {
    const data = {
      username: this.username,
      password: password
    }

    const headers = {headers: {'Access-Control-Allow-Origin': '*'}};
    return axios.post(this.backendUrl + 'login', data, headers)
      .then(response => {
        return response.data;
      })
      .catch(error => {
        console.log(error);
        return {'response': 'FAILURE'};
      });
  }

  setUsername() {
    const inputs = document.getElementsByClassName('username');
    const input = inputs[inputs.length - 1];
    const span = input.parentNode;
    const username = input.value;

    span.removeChild(input);
    span.innerHTML += username;

    this.username = username;
  }

  onUsernameEnter(e) {
    if (e.key === 'Enter') {
      this.setUsername();
      const passwords = document.getElementsByClassName('password');
      const password = passwords[passwords.length - 1];
      password.parentNode.classList.remove('hidden');
      password.focus();
    } else if (e.ctrlKey && e.key === 'c') {
      this.props.onEnter(null, null);
      return;
    }
  }

  onPasswordEnter(e) {
    if (e.key === 'Enter') {
      const password = e.currentTarget.value;
      const inputs = document.getElementsByClassName('password');
      const input = inputs[inputs.length - 1];
      const span = input.parentNode;

      span.removeChild(input);
      span.innerHTML += '';

      if (this.username === undefined || this.username === null) {
        this.setUsername();
      }

      this.backendLogin(password).then(message => {
        if (message['response'] === 'FAILURE') {
          this.props.onEnter(null, null);
        } else {
          this.props.onEnter(this.username, message['token']);
        }
      });
    } else if (e.ctrlKey && e.key === 'c') {
      this.props.onEnter(null, null);
      return;
    }
  }

  render() {
    if (this.props.token !== null)  {
      return (
        <div>
          <span>username:
            <input
              className="username cmd"
              onKeyDown={this.onUsernameEnter.bind(this)}
              type='text'
              autoFocus>
              </input>
          </span>
          <br />
          <span className="hidden">password:
            <input
              className="password cmd"
              onBlur={this.setFocus}
              onKeyDown={this.onPasswordEnter.bind(this)}
              type='password'
              autoFocus>
              </input>
          </span>
        </div>
      );
    } else {
      this.props.onEnter(null, this.props.token);
      return <div></div>;
    }
  }
}

export default Login;
