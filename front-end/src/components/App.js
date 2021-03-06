import React, { Fragment } from 'react'
import '../index.css'

import {
  Card,
  Carousel,
  message,
  Row,
  Tabs,
  Table,
  Col,
  Avatar,
  Icon,
  Modal
} from 'antd'

import Game from './Game'
import Tournament from './Tournament'

const TabPane = Tabs.TabPane;


function tabsCallBack(key) {
  console.log(key);
}


class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      groups: [],
      today: [],
      tmr: [],
      now: [],
      news: [],
      modal: {
        open: false,
        title: "Game",
        content: <h1>Loading...</h1>
      }
    }

    this.getDataAs('https://world-cup-json.herokuapp.com/matches/today', "today", "Today")
    this.getDataAs('https://world-cup-json.herokuapp.com/matches/tomorrow', "tmr", "Tomorrow")
    setInterval(() => {
      this.getDataAs('https://world-cup-json.herokuapp.com/matches/today', "today", "Today")
      this.getDataAs('https://world-cup-json.herokuapp.com/matches/tomorrow', "tomorrow", "Tomorrow")
    }, 60 * 1000)
  }

  async getDataAs(apiUrl, label, name, modifier) {
    try {
      const response = await fetch(apiUrl);
      const json = await response.json();
      const obj = {};

      if (modifier != null) {
        obj[label] = modifier(json)
      } else {
        obj[label] = json
      }
      this.setState((prev, props) => Object.assign({}, prev, obj))
    } catch (e) {
      message.error(`${name} data error`);
      console.error(e)
    }
  }

  renderGames(t) {
    const { today } = this.state;
    const { tmr } = this.state;
    if (today.length > 0 && t == 1) {
      return (
        <Fragment >
          {today.map((match, i) => (
            <Col key={i} span={6}>
              <Game match={match} modal={this.openModal.bind(this)}/>
            </Col>
          ))}
        </Fragment>
      )
    }
    if (tmr.length > 0 && t == 0) {
      return (
        <Fragment >
          {tmr.map((match, i) => (
            <Col key={i} span={6}>
              <Game match={match} modal={this.openModal.bind(this)}/>
            </Col>
          ))}
        </Fragment>
      )
    }
    return <br/>
  }

  openModal(title, content) {
    this.setState((prev, props) => (
      Object.assign(prev, {
        modal: {
          open: true,
          title,
          content
        }
      })
    ))
  }

  render() {
    let now = {};
    if (this.state.now.length > 0) {
      now = this.state.now[0]
    } else {
      now = this.state.today.filter(match => match.status != 'completed')[0]
      if (now == null) {
        now = this.state.today[this.state.today.length - 1]
      }
    }
    return (
      <div id="main">
        <Modal
          width="90%"
          title={this.state.modal.title}
          visible={this.state.modal.open}
          onOk={() => this.setState((prev, props) => (Object.assign(prev, { modal:{ open: !prev.modal.open }})))}
          onCancel={() => this.setState((prev, props) => (Object.assign(prev, { modal:{ open: !prev.modal.open }})))}
        >
          {this.state.modal.content}
        </Modal>
            <div style={mainContent}>
            <div id="header" style={{ textAlign: 'center', padding: 10 }}>
                <h1 style={{ margin: 0 }}>World Cup 2018 Live</h1>
            </div>

            <Tabs defaultActiveKey="1" onChange={tabsCallBack}  style={{ height: "100%" }}>
              <TabPane tab="Prediction" key="1">

                <Row gutter={16}>
                  <Icon type="github" spin={true} style={{ fontSize: 30, color: '#08c', width: "100%" }} />
                </Row>
                <Row gutter={16}>
                <Col style={{ marginTop: "auto", marginBottom: "auto" }}>
                  {this.renderGames(1)}
                </Col>
                <Col style={{ marginTop: "auto", marginBottom: "auto" }}>
                  {this.renderGames(0)}
                </Col>
                </Row>
                <Row gutter={16}>
                    <Tournament />
                </Row>

              </TabPane>
              <TabPane tab="About" key="2">
              </TabPane>
            </Tabs>

            </div>
      </div>
    );
  }
}

const mainContent = {
  width: "calc(100% - 200px)",
  height: "100vh",
  display: "grid"
};

export default App;