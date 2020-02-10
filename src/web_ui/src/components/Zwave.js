import React from 'react';

export class Zwave extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="sensor">
                <h1>Z-Wave</h1>
                <pre className="sensor-data">
                    <code>
                        { this.props.data }
                    </code>
                </pre>
            </div>
        );
    }
}