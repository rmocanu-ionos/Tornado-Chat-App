import React from 'react';
import { Link } from 'react-router';

import Joi from 'joi';
import strategy from 'joi-validation-strategy';
import validation from 'react-validation-mixin';

import FormValidationError from './FormValidationError.react';
import WebSocketConnection from "../utils/WebSocketConnection";
import {history} from '../utils/History';


class Register extends React.Component {
    constructor(props) {
        super(props);

        this.validatorTypes = {
            username: Joi.string().required().label('Username'),
            password: Joi.string().required().label('Password')
        };

        this.state = {
            username: '',
            password: '',
        };

        this.onFormSubmit = this.onFormSubmit.bind(this);
    }

    getValidatorData() {
        return this.state;
    }

    onFormChange(name, event) {
        let value = event.target.value;
        this.state[name] = value;
        this.setState(this.state);
        this.props.validate(name);
    }

    onFormSubmit(event) {
        event.preventDefault();
        this.props.validate((error) => {
            if (!error) {
                // CALL BACKEND API
                let wsConnection = new WebSocketConnection();
                wsConnection.send({
                    verb: 'post',
                    url: '/register',
                    body: this.state
                }, payload => {
                    if (payload.status_code === 200) {
                        history.push('/login');
                    } else {
                        alert("Error " + payload.body.error);
                    }
                });
            }
        });
    }

    render() {
        return (
            <div className="container">
                <div className="col-sm-4"></div>
                <form onSubmit={this.onFormSubmit} className="form-horizontal col-sm-4">
                    <h1>Register</h1>
                    <hr />
                    <div className="form-group">
                        <label htmlFor="username" className="control-label">USERNAME</label>
                        <input type="text" ref="username" id="username"
                            className="form-control" placeholder="your username here"
                            value={this.state.username}
                            onChange={this.onFormChange.bind(this, 'username')}
                            onBlur={this.props.handleValidation('username')}/>
                        <FormValidationError key="form-errors-username" messages={this.props.getValidationMessages('username')}/>
                    </div>

                    <div className="form-group">
                        <label htmlFor="password" className="control-label">PASSWORD</label>
                        <input type="password" ref="password" id="password"
                            className="form-control" placeholder="&#8226;&#8226;&#8226;&#8226;&#8226;&#8226;&#8226;&#8226;"
                            value={this.state.password}
                            onChange={this.onFormChange.bind(this, 'password')}
                            onBlur={this.props.handleValidation('password')}/>
                        <FormValidationError key="form-errors-password" messages={this.props.getValidationMessages('password')}/>
                    </div>

                    <br />
                    <div className="form-group">
                        <input type="submit" value="Register" className="btn btn-info pull-right"/>
                    </div>
                </form>
                <div className="col-sm-4"></div>
            </div>
        )
    }
}

export default validation(strategy)(Register);
