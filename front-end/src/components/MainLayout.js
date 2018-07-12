import React, { Component, PropTypes } from 'react';
import { Link } from 'react-router-dom';
import { Menu, Icon } from 'antd';
import Tournament from './Tournament'


const SubMenu = Menu.SubMenu;

const MainLayout = () => {
    return (
      <div style={ normal }>
        <div style= { head }>
          <h1><Link to="/" style={{ color: 'white' }}>SportStats: 스포스탯츠 </Link></h1>
          <h2 style={{ color: 'white' }}>  빅데이터 기반 예측 서비스 </h2>
        </div>
        <div style={ content }>
          <div style={ side }>
            <Menu style={{ width: 240,background:'#FAFAFA' }} mode="inline" >
              <SubMenu key="sub1" title={<span><Icon type="appstore-o" /><span>축구</span></span>}>
                <Menu.Item key="1" style={{background:'#FAFAFA'}}><Link to="/worldcup">2018 World Cup</Link></Menu.Item>
              </SubMenu>
              <SubMenu key="sub2" title={<span><Icon type="bars" /><span>About</span></span>}>
                <Menu.Item key="3" style={{background:'#FAFAFA'}}><Link to="/about">About</Link></Menu.Item>
              </SubMenu>
            </Menu>
          </div>
          <div style={ main }>
            <h3 style={{ margin: 0 }}> 월드컵 16강 진출 국가의 우승 확률 </h3>
            <br />
            <br />
            <Tournament />
          </div>
        </div>
      </div>
    );
};

export default MainLayout;



const normal = {
  "display": "flex",
  "flexDirection": "column",
  "minHeight": "100%"
};

const head = {
  "background": "cadetblue",
  "padding": "1px 5px",
  "color": "#fff"
};

const content = {
  "flex": 1,
  "display": "flex"
};

const side = {
  "background": "#fafafa"
};

const main = {
  "padding": "3%",
  "flex": "1 0 auto",
  "borderLeft": "1px solid #e9e9e9",
  "marginLeft": "-1px"
};
