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
            name: Joi.string().required().label('name'),
            topic: Joi.string().required().label('topic')
        };

        this.state = {
            name: '',
            topic: '',
        };

        this.onFormSubmit = this.onFormSubmit.bind(this);
    }

    getValidatorData() {
        return this.state;
    }

    onFormChange(name, event) {
        this.state[name] = event.target.value;
        this.setState(this.state);
        this.props.validate(name);
    }

    onFormSubmit(event) {
        event.preventDefault();
        this.props.validate((error) => {
            if (!error) {
                // CALL BACKEND API
                ChatRooms.create({'name': this.state.name, 'topic': this.state.topic});
            }
        });
    }

    render() {
        return (
            <div className="row nopad">
                <form onSubmit={this.onFormSubmit} className="form-horizontal col-sm-4">
                    <h1>Create a room</h1>
                    <hr />
                    <div className="form-group">
                        <label htmlFor="name" className="control-label">Room name</label>
                        <input type="text" ref="name" id="name"
                            className="form-control" placeholder="Roomie"
                            value={this.state.name}
                            onChange={this.onFormChange.bind(this, 'name')}
                            onBlur={this.props.handleValidation('name')}/>
                        <FormValidationError key="form-errors-name" messages={this.props.getValidationMessages('name')}/>
                    </div>

                    <div className="form-group">
                        <label htmlFor="topic" className="control-label">Room topic</label>
                        <input type="text" ref="topic" id="topic"
                            className="form-control" placeholder="&#8226;&#8226;&#8226;&#8226;&#8226;&#8226;&#8226;&#8226;"
                            value={this.state.topic}
                            onChange={this.onFormChange.bind(this, 'topic')}
                            onBlur={this.props.handleValidation('topic')}/>
                        <FormValidationError key="form-errors-topic" messages={this.props.getValidationMessages('topic')}/>
                    </div>

                    <br />
                    <div className="form-group">
                        <input type="submit" value="Create" className="btn btn-info pull-right"/>
                    </div>
                </form>
            </div>
        )
    }
}

export default validation(strategy)(Login);
