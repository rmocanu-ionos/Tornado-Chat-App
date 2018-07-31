import BaseStore from './BaseStore';

let chatRooms = null;

class ChatRooms extends BaseStore {

    constructor() {
        if (!chatRooms) {
            super();
            chatRooms = this;
        } else {
            return chatRooms;
        }

        this.baseuri = "/rooms/";
        this.registerActions();
    }
}

export default new ChatRooms();
