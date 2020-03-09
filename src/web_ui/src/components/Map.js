import React from 'react';
import '../App.css';
import './Map.css';
import { ReactComponent as H2alsvMap } from './../h2alsv_map.svg';
import { ReactComponent as UserIcon } from './../user_icon.svg';

function getCoordinates(x, y) {
    let x_cord = 20*x*Math.random();
    x_cord = x_cord.toString()+'%';
    let y_cord = 20*x*Math.random();
    y_cord = y_cord.toString()+'%';
    console.log(x_cord, y_cord);
    return [x_cord, y_cord];
}

export class Map extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            userIconTop: '20%',
            userIconLeft: '50%',
        };
        this.handlerClick = this.handlerClick.bind(this);
    }

    handlerClick() {
        let coords = getCoordinates(2, 3);
        console.log(coords);
        this.setState(state => ({
            userIconTop: coords[1],
            userIconLeft: coords[0],
        }));
    }

    render() {
        return (
            <div className="map">
                <p> hej</p>
                <button onClick={this.handlerClick}>yoy</button>
                <div className="map-wrapper">
                    <H2alsvMap />
                    <UserIcon id="user_icon" className="userIcon" style={{top: this.state.userIconTop, left: this.state.userIconLeft}}/>
                </div>
            </div>
        );
    }
}