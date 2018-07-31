import React from 'react';
import { Link } from 'react-router';

import Joi from 'joi';
import strategy from 'joi-validation-strategy';
import validation from 'react-validation-mixin';

import WebSocketConnection from '../../utils/WebSocketConnection';
import FormValidationError from '../FormValidationError.react';
import ChatRooms from '../../stores/ChatRooms';
import {history} from '../../utils/History';


class Login extends React.Component {
    constructor(props) {
        super(props);

        this.validatorTypes = {
            id: Joi.string().required().label('id')
        };

        this.state = {
            id: ''
        };

        this.onFormSubmit = this.onFormSubmit.bind(this);
    }

    getValidatorData() {
        return this.state;
    }

    onFormChange(id, event) {
        this.state[id] = event.target.value;
        this.setState(this.state);
        this.props.validate(id);
    }

    onFormSubmit(event) {
        event.preventDefault();
        this.props.validate((error) => {
            if (!error) {
                // CALL BACKEND API
                ChatRooms.deleteByid(this.state.id);
            }
        });
    }

    render() {
        return (
            <div className="row nopad">
                <form onSubmit={this.onFormSubmit} className="form-horizontal col-sm-4">
                    <h1>DELETE a room</h1>
                    <hr />
                    <div className="form-group">
                        <label htmlFor="name" className="control-label">Room name</label>
                        <input type="text" ref="name" id="text"
                            className="form-control" placeholder="room_id"
                            value={this.state.id}
                            onChange={this.onFormChange.bind(this, 'id')}
                            onBlur={this.props.handleValidation('id')}/>
                        <FormValidationError key="form-errors-name" messages={this.props.getValidationMessages('id')}/>
                    </div>


                    <br />
                    <div className="form-group">
                        <input type="submit" value="Delete" className="btn btn-info pull-right"/>
                    </div>
                </form>
            </div>
        )
    }
}

export default validation(strategy)(Login);
