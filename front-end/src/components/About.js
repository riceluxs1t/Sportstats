import { Layout } from 'antd';
import React from 'react'


const { Header, Footer, Sider, Content } = Layout;

const layoutStyle = {
  height: "768px",
}


export default function About(props) {
    return(
        <Layout size={{layoutStyle}} >
          <Header>Header</Header>
          <Content>Content</Content>
          <Footer>Footer</Footer>
        </Layout>
    )
};