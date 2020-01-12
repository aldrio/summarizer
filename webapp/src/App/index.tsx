import React from 'react'
import 'utils/typography'
import styles from './styles'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from 'react-router-dom'
import { Frontpage } from 'pages/Frontpage'
import { Summary } from 'pages/Summary'

type Props = {}
export const App: React.FC<Props> = () => {
  return (
    <Router>
      <Switch>
        <Route exact path="/s/:url+">
          <Summary />
        </Route>
        <Route exact path="/">
          <Frontpage />
        </Route>
        <Route>
          <Redirect to="/" />
        </Route>
      </Switch>
    </Router>
  )
}
