import { Dispatcher } from 'flux';

let appDispatcher = null;


class AppDispatcher extends Dispatcher {
    constructor() {
        if (!appDispatcher) {
            super();
            appDispatcher = this;
        } else {
            return appDispatcher;
        }

        this.registeredCallbacks = [];
    }

    registerOnce(action, callback) {

        if (this.registeredCallbacks.indexOf(action) === -1) {
            this.registeredCallbacks.push(action);

            return this.register(function (payload) {
                if (payload.action === action) {
                    callback(payload);
                }
            });
        }
    }
}

export default new AppDispatcher();
