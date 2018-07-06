import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter, Switch, Route } from 'react-router-dom'

import App from './components/App'
import About from './components/About'
import MainLayout from './components/MainLayout'

ReactDOM.render((
  <BrowserRouter>
    <Switch>
      <Route exact path='/' component={MainLayout}/>
      <Route exact path='/worldcup' component={App}/>
      <Route exact path='/about' component={About}/>
      <Route path='*' component={MainLayout}/>
    </Switch>
  </BrowserRouter>
), document.getElementById('root'));
