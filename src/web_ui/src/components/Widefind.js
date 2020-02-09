import React from 'react';

export class Widefind extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="sensor">
                <h1>Widefind placeholder</h1>
                <h2>{this.props.data}</h2>
            </div>
        );
    }
}