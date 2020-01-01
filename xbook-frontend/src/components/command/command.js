import React from 'react';
import './command.scss';

const axios = require('axios');
const backend_url = 'http://localhost:8080/';

class Command extends React.Component {

  setFocus() {
    setTimeout(() => {
      document.getElementsByClassName('cmd')[0].focus();
    }, 5);
  }

  accessBackend(command) {
    return axios.post(backend_url + 'execute', {'command': command}, {headers: {'Access-Control-Allow-Origin': '*'}}).then(response => {
      let message = 'DEFAULT MESSAGE';
      if (response['status'] === 200) {

      } else {
        message = 'This input was not handled!';
      }
      return message;
    });
  }

  execute(e) {
    if (e.key === 'Enter') {
      const command = e.currentTarget.value;
      let inputs = document.getElementsByClassName('cmd');
      const input = inputs[inputs.length - 1];
      const span = input.parentNode;
      span.removeChild(input);
      span.innerHTML += command;
      let message = 'Response Message';
      if (command === 'login') {
        this.facebookLogin();
      } else if (command === 'logout') {
        window.FB.logout(function(response) {
          console.log(response);
        });
      }
      this.accessBackend(command).then(message => {
        this.props.onEnter(message);
      });
    }
  }

  componentDidMount() {
    document.addEventListener('FBObjectReady', this.initializeFacebookLogin);
  }

  componentWillUnmount() {
    document.removeEventListener('FBObjectReady', this.initializeFacebookLogin);
  }

  /**
   * Init FB object and check Facebook Login status
   */
  initializeFacebookLogin = () => {
    this.FB = window.FB;
    this.checkLoginStatus();
  }

  /**
   * Check login status
   */
  checkLoginStatus = () => {
    this.FB.getLoginStatus(this.facebookLoginHandler);
  }

  /**
   * Check login status and call login api is user is not logged in
   */
  facebookLogin = () => {
    if (!this.FB) return;

    this.FB.getLoginStatus(response => {
      if (response.status === 'connected') {
        this.facebookLoginHandler(response);
      } else {
        const scopeText = `
          email,
          groups_access_member_info,
          publish_to_groups,
          user_age_range,
          user_birthday,
          user_friends,
          user_gender,
          user_hometown,
          user_likes,
          user_link,
          user_location,
          user_photos,
          user_posts,
          user_videos`;
        this.FB.login(this.facebookLoginHandler, {scope: scopeText});
      }
    }, );
  }

  /**
   * Handle login response
   */
  facebookLoginHandler = response => {
    if (response.status === 'connected') {
      this.FB.api('/me', userData => {
        let result = {
          ...response,
          user: userData
        };
        this.props.onLogin(true, result);
      });
    } else {
      this.props.onLogin(false);
    }
  }

  render() {
    let {children} = this.props;
    return (
      <span>&gt;&gt;&gt;&nbsp;
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
