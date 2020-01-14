import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

import './App.scss';

import Command from './components/command/command';
import Response from './components/response/response';
import Login from './components/login/login';
import Register from './components/register/register';
import Policy from './components/policy/policy';

class App extends React.Component {

  components = [];
  state = {
    username: null,
    token: null
  };

  constructor(props) {
    super(props);
    this.components.push(<Command
      key='0'
      onEnter={this.handleCommand.bind(this)}
      token={this.props.token}></Command>);
  }

  displayResponse(message) {
    this.components.push(<Response
      key={this.components.length}
      mess={message}></Response>);
  }

  displayCommand() {
    this.components.push(<Command
      key={this.components.length}
      onEnter={this.handleCommand.bind(this)}
      username={this.state.username}
      token={this.state.token}></Command>);
  }

  handleCommand(message) {
    switch (message) {
      case 'login':
        this.components.push(<Login
          key={this.components.length}
          onEnter={this.handleLogin.bind(this)}></Login>);
        break;
      case 'register':
        this.components.push(<Register
          key={this.components.length}></Register>)
      case 'logout':
        this.state = {
          username: null,
          token: null
        };
        message = 'Successful ' + message;
      default:
        this.displayResponse(message);
        this.displayCommand();
    }
    this.forceUpdate();
  }

  handleLogin(username, token) {
    console.log(username, token);
    if (username === null && token === null) {
      this.displayResponse('Incorrect username or password');
    } else {
      this.setState({
        username: username,
        token: token,
      });
      this.displayResponse('Successful Login');
    }
    this.displayCommand();
    this.forceUpdate();
  }

  handleLogin(flag, username, token) {
    switch (flag) {
      case 0:
        this.displayResponse('Username already taken.');
        break;
      case 1:
        this.displayResponse('Backend Error');
        break;
      case 2:
        this.handleLogin(username, token);
    }
  }

  render() {
    return (
      <div className="App">
        <Router>
          <Switch>
            <Route path='/' exact>
              {this.components}
            </Route>
            <Route path='/policy' component={Policy} />
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
