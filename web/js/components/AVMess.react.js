import React from 'react';
import { Router, Route, IndexRoute } from 'react-router';

import NotFound from './NotFound.react';
import ChatApp from './layout/ChatApp.react';
import Login from './Login.react';
import Register from './Register.react';
import { history } from '../utils/History';
import AuthStore from '../stores/AuthStore';
import ChatRoom from "./layout/ChatRoom.react";
import ChatRoomForm from './layout/ChatRoomForm.react';
import ChatRoomFormDelete from './layout/ChatRoomFormDelete.react'


function getInitialAppState() {
    return {
        feeds: []
    }
}

class AviraMessenger extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    getAppState() {
        let state = JSON.parse(localStorage.getItem('state'));
        if (!state) {
            state = getInitialAppState();
        }

        return state;
    }

    setAppState(state) {
        localStorage.setItem('state', JSON.stringify(state));
    }

        /**
     * Middleware that checks if user is authenticated; if not redirect to /login
     */
    requireAuth(nextState, replaceState, callback) {
        if (!AuthStore.isLoggedIn()) {
            // replaceState({nextPathname: nextState.location.pathname}, '/login');
            replaceState('/login');
        }

        callback();
    }

    render() {
        return (
            <Router history={history}>
                <Route path="/" component={ChatApp} onEnter={this.requireAuth}>
                    <Route path="rooms/create" component={ChatRoomForm}/>
                    <Route path="rooms/delete" component={ChatRoomFormDelete}/>
                    <Route path="rooms/:id" component={ChatRoom}/>
                </Route>
                <Route path="/login" component={Login}/>
                <Route path="/register" component={Register}/>
                <Route path="*" component={NotFound} />
            </Router>
        );
    }
}

export default AviraMessenger;
