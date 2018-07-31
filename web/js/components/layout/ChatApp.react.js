import React from 'react';
import { Link } from 'react-router';

import TopBar from './TopBar.react';
import ChatRooms from '../../stores/ChatRooms';
import Notifications from '../../stores/Notifications';


class ChatApp extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            chatRooms: []
        };

        this._onChatRoomsChange = this._onChatRoomsChange.bind(this);
        this._onNotification = this._onNotification.bind(this);
    }

    componentDidMount() {
        ChatRooms.addListener(this._onChatRoomsChange);
        Notifications.addListener(this._onNotification);

        ChatRooms.fetchAll();
    }

    componentWillUnmount() {
        ChatRooms.removeListener(this._onChatRoomsChange);
        Notifications.removeListener(this._onNotification);
    }

    _onChatRoomsChange() {
        console.log("Chat Rooms updated");
        this.setState({chatRooms: ChatRooms.all});
    }

    _onNotification() {
        Notifications.display();
    }

    render() {
        console.log(this.state.chatRooms);
        return (
            <div className="container-fluid">
                <div className="row">
                    <TopBar />
                </div>
                <div className="container">
                    <div className="row">
                        <div className="col-sm-3 nopad">
                            <h3>Rooms:</h3>
                            <ul>
                                {
                                    this.state.chatRooms.map((room, i) => {
                                        return (
                                            <li key={`room-link-${i}`} >
                                                <Link to={`/rooms/${room.id}`}>
                                                    {room.name}
                                                </Link>
                                            </li>
                                        );
                                    })
                                }
                            </ul>
                            <Link to={`/rooms/create`}>Create room</Link>
                            <br/>
                            <Link to={`/rooms/delete`}>Delete room</Link>
                        </div>
                        <div className="col-sm-9 nopad">
                            <div className="row">
                                {this.props.children}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default ChatApp;
