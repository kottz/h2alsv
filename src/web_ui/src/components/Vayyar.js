import React from 'react';

export class Vayyar extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const test_json = { 
            time: 5,
            sensor_type: "vayyar",
            data: {
                posture_vector: "Standing",
                x_coordinate: "24.5",
                y_coordinate: "28.8",
                z_coordinate: "29.2",
            }
        }
        return (
            <div className="sensor">
                <h1>Vayyar</h1>
                {/*<h2>{this.props.data}</h2>*/}
                <pre className="sensor-data">
                    <code>
                        { this.props.data }
                    </code>
                </pre>
            </div>
        );
    }
}