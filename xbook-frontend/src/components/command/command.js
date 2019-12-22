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

  execute(e) {
    if (e.key === 'Enter') {
      const command = e.currentTarget.value;
      axios.post(backend_url + 'execute', {'command': command}).then(response => {
        if (response['status'] === 200) {

        } else {
          //handle failure
        }
      });
    }
  }

  render() {
    return <span>&gt;&gt;&gt;
            <input
              className='cmd'
              onBlur={this.setFocus}
              onKeyDown={this.execute}
              type='text'
              autoFocus>
            </input>
           </span>;
  }
}

export default Command;
