import React from 'react';
import jwt_decode from 'jwt-decode';

import BaseStore from './BaseStore';
import WebSocketConnection from '../utils/WebSocketConnection';

let authStore = null;

class AuthStore extends BaseStore {

    constructor() {
        if (!authStore) {
            super();
            authStore = this;
        } else {
            return authStore;
        }

        this._error = null;
    }

    login(data) {
        let wsConnection = new WebSocketConnection();
        wsConnection.send({
            verb: 'post',
            url: '/login',
            body: {
                username: data.username,
                password: data.password
            }
        }, payload => {
            if (payload.status_code === 200) {
                this.save(payload.body.data);
            }
        });
    }

    register(data) {
        let wsConnection = new WebSocketConnection();
        wsConnection.send({
            verb: 'post',
            url: '/register',
            body: {
                username: data.username,
                password: data.password
            }
        }, payload => {
            if (payload.status_code === 200) {
                this.save(payload.body.data);
            }
        });
    }

    save(data) {
        localStorage.setItem('token', data.token);
        this.emitChange();
    }

    set error(error) {
        this._error = error;
        if (error) {
            this.emitChange();
        }
    }

    get error() {
        return this._error;
    }

    get userId() {
        let id = null;
        try {
            id = jwt_decode(this.token).uid;
        } catch (e) {

        }
        return id
    }

    get token() {
        return localStorage.getItem('token');
    }

    isLoggedIn() {
        return !!localStorage.getItem('token');
    }
}

export default new AuthStore();
