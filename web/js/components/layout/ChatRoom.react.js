import React from 'react';

import Message from './Message.react';
import Messages from '../../stores/Messages';
import ChatRooms from '../../stores/ChatRooms';

import WebSocketConnection from "../../utils/WebSocketConnection";

class ChatRoom extends React.Component {
    constructor(props) {
        super(props);

        this.roomId = props.params.id;
        this.state = {
            unfinishedMessage: '',
            messages: [],
            room: null
        };

        this._onRoomChange = this._onRoomChange.bind(this);
        this._onMessagesChange = this._onMessagesChange.bind(this);
        this._onSend = this._onSend.bind(this);
        this._onMessageEdit = this._onMessageEdit.bind(this);
    }

    componentWillReceiveProps(nextProps) {
        let newState = {'messages': []};
        if (this.roomId !== nextProps.params.id) {
            newState['unfinishedMessage'] = '';
            newState['room'] = null;
        }
        this.roomId = nextProps.params.id;
        this.setState(newState, () => {
            ChatRooms.fetchById(this.roomId);
            this.connect();
        });
    }

    componentDidMount() {
        Messages.addListener(this._onMessagesChange);
        ChatRooms.addListener(this._onRoomChange);
        ChatRooms.fetchById(this.roomId);
        this.connect();
        console.log("Fetching messages for room", this.roomId);
    }

    componentWillMount() {
        Messages.removeListener(this._onMessagesChange);
        ChatRooms.removeListener(this._onRoomChange);
    }

    _onMessagesChange() {
        this.setState({messages: Messages.filter(this.roomId)});
        let objDiv = document.getElementById("room-messages");
        objDiv.scrollTop = objDiv.scrollHeight;
    }

    _onSend(e) {
        e.preventDefault();
        console.log("Preparing to send", this.state.unfinishedMessage);
        // send message
        Messages.create({room_id: parseInt(this.roomId), message: this.state.unfinishedMessage});
        this.setState({unfinishedMessage: ''});
    }

    _onMessageEdit(e) {
        this.setState({unfinishedMessage: e.target.value});
    }

    _onRoomChange() {
        this.setState({room: ChatRooms.getById(this.roomId)});
    }

    connect() {
        let wsConnection = new WebSocketConnection();

        wsConnection.send({
            verb: 'post',
            url: '/connect',
            body: {
                room_id: parseInt(this.roomId)
            }
        }, payload => {
            console.log("Received on /connect", payload);
            if (payload.status_code === 200) {
                Messages.fetchRoomMessages(this.roomId);
            }
            else {
                console.log(payload);
            }
        });
    }

    render() {
        return (
            <div className="row nopad" style={styles.wrapper}>
                <div className="row nopad">
                    <h3>Messages: <small>{this.state.room ? this.state.room.topic : 'No topic'}</small></h3>
                </div>
                <div id="room-messages" className="row nopad" style={{maxHeight: '300px', overflow: 'scroll'}}>
                    {
                        this.state.messages.map((message, i) => {
                            return (
                                <Message key={'message-' + i} message={message}/>
                            );
                        })
                    }
                </div>
                <div className="row nopad">
                    <form onSubmit={this._onSend} className="input-group">
                        <input onChange={this._onMessageEdit} value={this.state.unfinishedMessage} type="text" className="form-control" placeholder="Type here..."/>
                        <span className="input-group-btn">
                            <button className="btn btn-default" type="submit">Send</button>
                        </span>
                    </form>
                </div>
            </div>
        )
    }
}

const styles = {
    wrapper: {
        'minHeight': '100px'
    }
};

export default ChatRoom;
