import React from 'react';


class Message extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            message: this.props.message
        }
    }

    render() {
        return (
            <div className="row nopad">
                <p>created_at: {this.state.message.created_at}</p>
                <p>user: {this.state.message.user_id}</p>
                <p>data: {this.state.message.data}</p>
                <hr/>
            </div>
        )
    }
}

export default Message;
