import React from 'react';

export class SensorStatus extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="sensor">
                <h1>Sensor Status placeholder</h1>
                <h2>{this.props.data}</h2>
            </div>
        );
    }
}