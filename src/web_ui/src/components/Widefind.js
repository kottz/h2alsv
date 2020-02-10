import React from 'react';

export class Widefind extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="sensor">
                <h1>WideFind</h1>
                <pre className="sensor-data">
                    <code>
                        { this.props.data }
                    </code>
                </pre>
            </div>
        );
    }
}