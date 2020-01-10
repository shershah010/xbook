import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

import './App.scss';

import Command from './components/command/command';
import Response from './components/response/response';
import Policy from './components/policy/policy';
import Login from './components/login/login';

class App extends React.Component {

  displayData = [];
  state = {
    username: null,
    token: null,
    messages: []
  };

  handleCommand(message) {
    this.state.messages.push(message);
    this.setState({
      messages: this.state.messages
    });
  }

  handleLogin(username, token) {
    this.state.messages.push('Successful Login');
    this.setState({
      username: username,
      token: token,
      messages: this.state.messages
    });
  }


  render() {
    const children = [];

    for (let i = 0; i < this.state.messages.length; i += 1) {
      if (this.state.messages[i] === 'login') {
          children.push(<Login key={i + 'b'} onEnter={this.handleLogin.bind(this)}></Login>);
      } else {
        children.push(<Response key={i + 'a'} mess={this.state.messages[i]}></Response>);
        children.push(<Command key={i + 'b'} onEnter={this.handleCommand.bind(this)} username={this.state.username}></Command>);
      }
    }

    return (
      <div className="App">
        <Router>
          <Switch>
            <Route path='/' exact>
              <Command onEnter={this.handleCommand.bind(this)}></Command>
              {children}
            </Route>
            <Route path='/policy' component={Policy} />
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
