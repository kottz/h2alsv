import React from 'react';
import '../App.css';
import './Map.css';
import { ReactComponent as H2alsvMap } from './../h2alsv_map.svg';
import { ReactComponent as UserIcon } from './../user_icon.svg';

function getCoordinates(x, y) {
    let x_cord = 20*x;
    x_cord = x_cord.toString()+'%';
    let y_cord = 20*y;
    y_cord = y_cord.toString()+'%';
    console.log(x_cord, y_cord);
    return [x_cord, y_cord];
}

function getCoordinatesTest(x, y) {
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
        let coords = getCoordinatesTest(2, 3);
        console.log(coords);
        this.setState(state => ({
            userIconTop: coords[1],
            userIconLeft: coords[0],
        }));
    }

    render() {
        return (
            <div className="map">
                <h2>Map</h2>
                <div className="map-wrapper">
                    <H2alsvMap />
                    <UserIcon id="user_icon" className="userIcon" style={{top: this.props.vayyar_location_matrix[1], left: this.props.vayyar_location_matrix[0]}}/>
                </div>
            </div>
        );
    }
}