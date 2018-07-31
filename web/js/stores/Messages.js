import BaseStore from './BaseStore';
import AppDispatcher from "../utils/AppDispatcher";
import WebSocketConnection from "../utils/WebSocketConnection";

let messages = null;

class Messages extends BaseStore {

    constructor() {
        if (!messages) {
            super();
            messages = this;
        } else {
            return messages;
        }

        this.instancesByRoom = {};
        this.baseuri = "/messages/";
        this.registerActions();
    }

    filter(chatRoomId) {
        let items = this.instancesByRoom[chatRoomId] || [];
        items.sort(function (a, b) {
            return new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
        });
        return items;
    }

    _addInstance(instance) {
        if (!this.instancesByRoom[instance.room_id]) {
            this.instancesByRoom[instance.room_id] = []
        }
        this.instancesByRoom[instance.room_id].push(instance);
        super._addInstance(instance);
    }

    fetchRoomMessages(roomId) {
        this.instancesByRoom[roomId] = [];
        let wsConnection = new WebSocketConnection();

        wsConnection.send({
            verb: 'get',
            url: this.baseuri,
            args: {
                room_id: parseInt(roomId)
            }
        }, payload => {
            payload.body.data.map(item => {
                this._addInstance(item);
            });
            this.emitChange();
        });
    }
}

export default new Messages();
