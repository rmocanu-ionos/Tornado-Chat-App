import BaseStore from './BaseStore';
import AppDispatcher from '../utils/AppDispatcher';

let notifications = null;

class Notifications extends BaseStore {

    constructor() {
        if (!notifications) {
            super();
            notifications = this;
        } else {
            return notifications;
        }

        this.baseuri = "/notifications/";

        this.instances = [];

        // register gui related actions
        AppDispatcher.registerOnce('POST notifications', payload => {
            this.push(payload);
        });
    }

    push(payload) {
        if (payload.verb === 'POST') {
            this.instances.push(payload);
            this.emitChange();
        }
    }

    pop() {
        return this.instances.pop();
    }

    display() {
        let notif = this.pop();
        while (notif) {
            let data = notif.body.data || {};
            alert("Notification:" + data);
            notif = this.pop();
        }
    }
}

export default new Notifications();
