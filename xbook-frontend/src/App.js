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

class App extends React.Component {

  displayData = [];
  state = {
    username: null,
    messages: []
  };

  onFacebookLogin = (loginStatus, resultObject) => {
    if (loginStatus === true) {
      this.setState({
        username: resultObject.user.name
      });
    } else {
      console.log('Facebook login error');
    }
  }

  onEnter = (message) => {
    this.state.messages.push(message);
    this.setState({
      messages: this.state.messages
    })
  }

  render() {
    const { username } = this.state;
    const children = [];

    for (let i = 0; i < this.state.messages.length; i += 1) {
      children.push(<Response key={i + 'a'} mess={this.state.messages[i]}></Response>);
      children.push(<Command key={i + 'b'} onLogin={this.onFacebookLogin} onEnter={this.onEnter}></Command>);
    }

    return (
      <div className="App">
        <Router>
          <Switch>
            <Route path='/' exact>
              <Command onLogin={this.onFacebookLogin} onEnter={this.onEnter}></Command>
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
