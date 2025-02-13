import React, { Component } from 'react'
import Instructions from './Instructions'
import Contact from './Contact'
import Counter from './Counter'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      contacts: [
        {id: 1, name: "Angad", nickname: "greg", hobby: "dirty-ing"},
        {id: 2, name: "Roy", nickname: "uwu", hobby: "weeb"},
        {id: 3, name: "Daniel", nickname: "oppa", hobby: "losing money with options trading"},
      ]
    }
  }

  render() {
    return (
      <div className="App">
        <Instructions complete = {true} />
        <Counter count = {0} />

        {this.state.contacts.map(x => (<Contact id={x.id} name={x.name} nickname={x.nickname} hobby={x.hobby} />))}


        </div>
    )
  }
}


export default App
