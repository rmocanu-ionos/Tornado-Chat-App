'use strict';

import config from '../config/Config';
import Utils from '../utils/Utils';
import AppDispatcher from '../utils/AppDispatcher';
import AuthStore from '../stores/AuthStore';

let connector = null;

class WebSocketConnection {

    /**
     * Creates connector instance.
     * @returns singleton instance
     */
    constructor() {
        // deal with the instance before starting to allocate resources
        if (!connector) {
            connector = this;
        } else {
            return connector;
        }

        this.connected = false;
        this.pendingRequests = [];
        this.pendingCallbacks = [];
        this.uniqueRequests = {};

        this.ws = null;
        this.connect();
    }

    connect() {
        if (!this.ws) {
            this.ws = new WebSocket(config.WS_URL);
            this.ws.onopen = WebSocketConnection.onOpen;
            this.ws.onmessage = WebSocketConnection.onMessage;
            this.ws.onclose = WebSocketConnection.onClose;
            this.ws.onerror = WebSocketConnection.onError;

            console.log("Socket connected!");
        }
    }

    /**
     * Implementation of ws.onopen
     * Send all pendingRequests to the backend.
     */
    static onOpen() {
        connector.connected = true;

        if (connector.pendingRequests.length > 0) {
            connector.pendingRequests.forEach(req => {
                this.send(JSON.stringify(req));
            });
            connector.pendingRequests = [];
        }
    }

    static onClose() {
        connector.ws = null;
        this.connected = false;
        console.log("Connection closed!");
    }

    static onError() {
        connector.ws = null;
        this.connected = false;
        console.log("Connection error!");
    }

    /**
     * Implementation of ws.onmessage
     * @param message
     */
    static onMessage(message) {
        connector.processMessage(JSON.parse(message.data));
    }

    /**
     * Processes a message and dispatches the appropriate payload.
     * @param message:
     */
    processMessage(message) {
        console.log('RECEIVED', message);
        if (message.hasOwnProperty('verb') && message.hasOwnProperty('url')) {
            let matches = message.url.match(/^(\/[a-z0-9\-_]*\/?).*$/i);
            let res = matches && matches[1];

            message.action = message.verb.toUpperCase() + ' ' + res;
            /**
             * If the includeRequestId flag was true when the message was sent
             * then we need to add the id in the payload
             */
            if (this.uniqueRequests[message.action + " " + message.id]) {
                message.action += ' ' + message.id;
            }
            console.log("Message action on receive", message.action);

            AppDispatcher.dispatch(message);

            /**
             * Delete the unique callback,
             * and unregister it from the AppDispatcher
             */
            if (this.uniqueRequests[message.action]) {
                AppDispatcher.unregister(this.uniqueRequests[message.action]);
                delete this.uniqueRequests[message.action];
            }
        }
    }

    /**
     * Send the request to server. Add to pendingRequests if connection is not yet available.
     * @param request:
     * @param callback: Callback function to register with AppDispatcher
     * @param includeRequestId: Adds the id in the action, before registering to AppDispatcher.
     *                          This is useful in case the same verb and resource are used for different purposes.
     * @returns request.id
     */
    send(request, callback, includeRequestId) {
        console.log('SENDING', request);
        if (this.ws && ~[2, 3].indexOf(this.ws.readyState) || !this.ws) {
            this.connected = false;
            this.connect();
        }

        request.id = Utils.uuid();

        // set authorization headers
        let headers = request.headers || {};
        let token = AuthStore.token;
        if (token) {
            headers['Authorization'] = 'Token ' + AuthStore.token;
        }
        request.headers = headers;
        if (callback) {
            //registering actions (removing resource id and everything after the resource name)
            let matches = request.url.match(/^(\/[a-z0-9\-_]*\/?).*$/i);
            let res = matches && matches[1];

            let action = request.verb.toUpperCase() + ' ' + res;
            // let action = res;
            console.log("Message action on send", action);
            action += includeRequestId ? ' ' + request.id : '';

            let registeredCallbackId = AppDispatcher.registerOnce(action, callback);

            if (includeRequestId) {
                this.uniqueRequests[action] = registeredCallbackId;
            }
        }

        if (!this.connected) {
            this.pendingRequests.push(request);
        } else {
            this.ws.send(JSON.stringify(request));
        }

        return request.id;
    }

    /**
     * Stops on-going request id and re-initializes the connection.
     * @param id
     */
    stopRequest(id) {
        this.ws.close();
        this.connect();
    }
}

export default WebSocketConnection;
