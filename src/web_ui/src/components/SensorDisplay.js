import React from 'react';
import { Vayyar } from './Vayyar';
import { Widefind } from './Widefind';
import { Zwave } from './Zwave';
import { SensorStatus } from './SensorStatus';
import './SensorDisplay.css';

export class SensorDisplay extends React.Component {
    constructor(props) {
        super(props)
        this.state = {vayyar: "My Vayyar Data",
            widefind: "My Widefind Data",
            zwave: "My Zwave Data",
            status: "My status Data", 
        };
        this.ws = new WebSocket('ws://localhost:3030/');

        this.ws.onmessage = msg => {
            this.setState({vayyar: msg.data});
            console.log(msg);
        }
    }
    render() {
        return (
            <div className="sensorDisplay">
                <Vayyar className="sensor" data={this.state.vayyar} />
                <Widefind data={this.state.widefind} />
                <Zwave data={this.state.zwave} />
                <SensorStatus data={this.state.status} />
            </div>
        );
    }
}