import React from 'react';
import '../App.css';

export class Footer extends React.Component {
    render() {
        return (
            <div className="App-footer">
                <p>Utvecklad med kärlek av grupp 1 | <a href="https://github.com/kottz/h2alsv">Github</a> | <a href="https://h2alsv.se">Docs</a></p>
            </div>
        );
    }
}