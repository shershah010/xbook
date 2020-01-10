import React from 'react';
import './login.scss';

const axios = require('axios');

class Login extends React.Component {

  username = null;
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

  backendLogin(password) {
    const data = {
      username: this.username,
      password: password
    }
    const headers = {headers: {'Access-Control-Allow-Origin': '*'}};
    return axios.post(this.backendUrl + 'login', data, headers)
      .then(response => {
        return response.data['response'];
      })
      .catch(error => {
        return 'BACKEND FAILURE! ' + error;
      });
  }

  onUsernameEnter(e) {
    if (e.key === 'Enter') {
      const username = e.currentTarget.value;
      const inputs = document.getElementsByClassName('username');
      const input = inputs[inputs.length - 1];
      const span = input.parentNode;

      span.removeChild(input);
      span.innerHTML += username;

      const passwords = document.getElementsByClassName('password');
      const password = passwords[passwords.length - 1];
      password.parentNode.classList.remove('hidden');
      password.focus();

      this.username = username;
    }
  }

  onPasswordEnter(e) {
    if (e.key === 'Enter') {
      this.backendLogin(e.currentTarget.value).then(message => {
        this.props.onEnter(this.username, message);
      });
    }
  }

  render() {
    return (
      <div>
        <span>username:
          <input
            className="username cmd"
            onBlur={this.setFocus}
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
  }
}

export default Login;
