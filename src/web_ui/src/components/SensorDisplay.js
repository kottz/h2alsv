import React from 'react';
import { Vayyar } from './Vayyar';
import { Widefind } from './Widefind';
import { Zwave } from './Zwave';
import { SensorStatus } from './SensorStatus';
import './SensorDisplay.css';

export class SensorDisplay extends React.Component {
    constructor(props) {
        super(props)
        this.state = {vayyar: "",
            widefind: "",
            zwave: "",
            status: "", 
        };
        this.ws = new WebSocket('ws://localhost:3030/');

        this.ws.onmessage = msg => {
            const json_msg = JSON.parse(msg.data);
            this.setState({[json_msg.sensor_type]: JSON.stringify(json_msg, null, 2)});
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