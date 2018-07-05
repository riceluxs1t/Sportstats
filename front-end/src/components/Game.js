import React, { Fragment } from 'react'
import { 
    Card, 
    Tag,
    Row,
    Col,
    Table,
    Button,
    Progress
} from 'antd'
import Flag from './Flag'
import LiveGame from './LiveGame'
import Stats from './Stats'
import moment from 'moment'
import { prediction_outcomes } from './predictions_outcomes'
import { prediction_brief } from './predictions_brief'

const { Meta } = Card

// const dataSource = prediction_outcomes['Uruguay-Portugal']

const columns = [{
  title: 'Match Outcome',
  dataIndex: 'outcome',
  key: 'outcome'
}, {
  title: 'Odds',
  dataIndex: 'prob',
  key: 'prob'
}];


const gridStyle = {
  width: '33%',
  textAlign: 'center',
};

function makeTag(match) {
    const { status, datetime } = match
    const time = new Date(datetime)
    if (status === "completed") {
        return (
            <Fragment>
                <Tag color="green">Completed</Tag>
                <br />
                {moment(time).fromNow()}
            </Fragment>
        )
    }
    if (status === "future") {
        return (
            <Fragment>
                <Tag color="orange">Up next</Tag>
                <br />
                {moment(time).fromNow()}
            </Fragment>
        )
    }
    return (
        <Fragment>
            <Tag color="red">Live</Tag>
            <br />
            {moment(time).fromNow()}
        </Fragment>
    )
}

export default class Game extends React.Component {
    handleModal() {
        const { modal } = this.props
        const { 
            home_team,
            home_team_statistics,
            away_team,
            away_team_statistics,
        } = this.props.match
        modal(`${home_team.country} vs. ${away_team.country}`, (
            <div style={{ 
                display: 'grid',
                gridTemplateColumns: "1fr 1fr 1fr"
            }}>
                <div>
                    <Stats team={home_team.country} stats={home_team_statistics}/>
                </div>
                <LiveGame match={this.props.match} mini={true} modal={() => { }} />
                <div>
                    <Stats team={away_team.country} stats={away_team_statistics}/>
                </div>
            </div>
        ))
    }

    render() {
        const { home_team, away_team, datetime, status } = this.props.match;
        const time = new Date(datetime);

        const prediction_key = home_team.country.concat('-').concat(away_team.country);
        const dataSource = prediction_outcomes[prediction_key];
        const brief = prediction_brief[prediction_key];
        return (
            <Card
                hoverable
                style={{ width: 240, margin: '10px auto' }}
                cover={
                    <div style={{ textAlign: "center" }}>
                        <Flag country={home_team.country} width={80} />
                        <Flag country={away_team.country} width={80} />
                        <p>{`${home_team.country} vs. ${away_team.country}`}</p>
                        <p>{`${time.getHours()}:${time.getMinutes()}${(() => { if (time.getMinutes() < 10) { return "0" } })()}`}</p>
                        {makeTag(this.props.match)}
                        <p>{home_team.goals} - {away_team.goals}</p>
                        {
                            this.props.match.home_team_statistics != null
                                ? <Button onClick={this.handleModal.bind(this)}>Details</Button>
                                : <Button disabled>Details coming soon</Button>
                        }

                        <br/>
                        <br/>

                        <Card title="Prediction">
                            <Card.Grid style={gridStyle}>Home</Card.Grid>
                            <Card.Grid style={gridStyle}>Draw</Card.Grid>
                            <Card.Grid style={gridStyle}>Away</Card.Grid>
                            <Card.Grid style={gridStyle}>{brief.win}</Card.Grid>
                            <Card.Grid style={gridStyle}>{brief.draw}</Card.Grid>
                            <Card.Grid style={gridStyle}>{brief.lose}</Card.Grid>
                        </Card>
                        <Table dataSource={dataSource} columns={columns}/>
                    </div>
                }
            >
            </Card>
        )
    }
}