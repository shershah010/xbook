import React from 'react';
import './register.scss';

const axios = require('axios');

class Register extends React.Component {

  data = null;
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

  backendRegister() {
    const headers = {headers: {'Access-Control-Allow-Origin': '*'}};
    return axios.post(this.backendUrl + 'register', this.data, headers)
      .then(response => {
        return response.data;
      })
      .catch(error => {
        console.log(error);
        return {'response': 'FAILURE', 'flag': 1};
      });
  }

  set(element) {
    const inputs = document.getElementsByClassName(element);
    const input = inputs[inputs.length - 1];
    const span = input.parentNode;
    const elVal = input.value;

    span.removeChild(input);
    span.innerHTML += elVal;

    this.data[element] = elVal;
  }

  show(element) {
    const elDOMs = document.getElementsByClassName(element);
    const elDOM = elDOMs[elDOMs.length - 1];
    elDOM.parentNode.classList.remove('hidden');
    elDOM.focus();
  }

  onFirstnameEnter(e){
    if (e.key === 'Enter') {
      this.set('firstname');
      this.show('lastname');
    }
  }

  onLastnameEnter(e) {
    if (e.key === 'Enter') {
      this.set('lastname');
      this.show('username');
    }
  }

  onUsernameEnter(e) {
    if (e.key === 'Enter') {
      this.set('username');
      this.show('password')
    }
  }

  onPasswordEnter(e) {
    if (e.key === 'Enter') {
      this.set('password');

      this.backendRegister().then(message => {
        if (message['response'] === 'FAILURE') {
          this.props.onEnter(message['flag'], null, null);
        } else {
          this.props.onEnter(message['flag'], this.data.username, message['token']);
        }
      });
    }
  }

  render() {
    if (this.props.token !== null)  {
      return (
        <div>
          <span>firstname:
            <input
              className="firstname cmd"
              onKeyDown={this.onFirstnameEnter.bind(this)}
              type='text'
              autoFocus>
              </input>
          </span>
          <br />
          <span>lastname:
            <input
              className="lastname cmd"
              onKeyDown={this.onLastnameEnter.bind(this)}
              type='text'
              autoFocus>
              </input>
          </span>
          <br />
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

export default Register;