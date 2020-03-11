import React from 'react';
import { Vayyar } from './Vayyar';
import { Widefind } from './Widefind';
import { Zwave } from './Zwave';
import { Map } from './Map';
import { SensorStatus } from './SensorStatus';
import './SensorDisplay.css';

function getMapCoordinates(x, y) {
    let x_cord = 20*x;
    x_cord = x_cord.toString()+'%';
    let y_cord = 20*y;
    y_cord = y_cord.toString()+'%';
    console.log(x_cord, y_cord);
    return [x_cord, y_cord];
}

export class SensorDisplay extends React.Component {
    constructor(props) {
        super(props)
        this.state = {vayyar: "",
            widefind: "",
            zwave: "",
            status: "", 
            vayyar_location_matrix: [],
        };
        this.ws = new WebSocket('ws://localhost:3030/');

        this.ws.onmessage = msg => {
            const json_msg = JSON.parse(msg.data);
            this.setState({[json_msg.sensor_type]: JSON.stringify(json_msg, null, 2)});
            if( json_msg.sensor_type === "vayyar" && json_msg.payload.ID === "BINARY_DATA") {
                let loc_matrix = json_msg.payload.Payload.LocationMatrix[0];
                let mapCoordinates = getMapCoordinates(loc_matrix[0], loc_matrix[1]);
                this.setState({vayyar_location_matrix: mapCoordinates});
            }
        }
    }

    render() {
        return (
            <div className="content">
                <div className="sensorDisplay">
                    <Vayyar className="sensor" data={this.state.vayyar} />
                    <Widefind data={this.state.widefind} />
                    <Zwave data={this.state.zwave} />
                    <SensorStatus data={this.state.status} />
                </div>
                <Map vayyar_location_matrix={this.state.vayyar_location_matrix} />
            </div>
        );
    }
}