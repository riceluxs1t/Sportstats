import React, { Fragment } from 'react'
import { Table } from 'antd'

const dataSource = JSON.parse(
    `
    [{"key": 1, "country": "Uruguay", "round1": "11.1%", "round2": "23.5%", "round4": "37.0%", "round8": "61.0%"}, {"key": 2, "country": "France", "round1": "9.0%", "round2": "17.6%", "round4": "29.2%", "round8": "62.3%"}, {"key": 3, "country": "Brazil", "round1": "8.0%", "round2": "10.9%", "round4": "34.0%", "round8": "74.1%"}, {"key": 4, "country": "Belgium", "round1": "12.9%", "round2": "21.0%", "round4": "47.5%", "round8": "77.6%"}, {"key": 5, "country": "Russia", "round1": "9.8%", "round2": "24.1%", "round4": "48.7%", "round8": "74.2%"}, {"key": 6, "country": "Croatia", "round1": "5.7%", "round2": "12.8%", "round4": "22.9%", "round8": "58.2%"}, {"key": 7, "country": "Switzerland", "round1": "6.8%", "round2": "15.4%", "round4": "28.9%", "round8": "54.8%"}, {"key": 8, "country": "Colombia", "round1": "4.4%", "round2": "10.6%", "round4": "25.9%", "round8": "62.5%"}, {"key": 9, "country": "Spain", "round1": "2.2%", "round2": "4.0%", "round4": "7.2%", "round8": "25.8%"}, {"key": 10, "country": "Denmark", "round1": "4.7%", "round2": "10.5%", "round4": "21.1%", "round8": "41.8%"}, {"key": 11, "country": "Portugal", "round1": "5.1%", "round2": "10.1%", "round4": "19.6%", "round8": "39.1%"}, {"key": 12, "country": "Argentina", "round1": "5.2%", "round2": "7.8%", "round4": "14.2%", "round8": "37.7%"}, {"key": 13, "country": "Mexico", "round1": "3.5%", "round2": "6.4%", "round4": "13.3%", "round8": "25.9%"}, {"key": 14, "country": "Sweden", "round1": "5.6%", "round2": "12.9%", "round4": "26.1%", "round8": "45.2%"}, {"key": 15, "country": "Japan", "round1": "1.7%", "round2": "2.8%", "round4": "5.1%", "round8": "22.4%"}, {"key": 16, "country": "England", "round1": "4.3%", "round2": "9.7%", "round4": "19.1%", "round8": "37.5%"}]
   `
)


const columns = [{
  title: 'Country',
  dataIndex: 'country',
  key: 'country',
}, {
  title: 'Round of 8',
  dataIndex: 'round8',
  key: 'round8',
}, {
  title: 'Semi Final',
  dataIndex: 'round4',
  key: 'round4'
}, {
  title: 'Final',
  dataIndex: 'round2',
  key: 'round2'
}, {
  title: 'Winning WC 2018',
  dataIndex: 'round1',
  key: 'round1'
}];


export default function Tournament() {
    return(
        <Table dataSource={dataSource} columns={columns} defaultExpandAllRows={ true } />
    )
}