import React, { Component } from 'react'

class Counter extends Component{
    state = {count: 0}

    addClick = () => {

        this.setState({count: this.state.count + 1})
    }
    subClick = () => {
        this.setState({count: this.state.count - 1})
    }
  // YOUR CODE GOES BELOW

  render() {
        const {count} = this.state
      return (
          <div>
              <label> {count} </label>
              <button onClick={this.addClick}> ADD </button>
              <button onClick={this.subClick}> SUB </button>

          </div>
    )
  }
}
export default Counter
