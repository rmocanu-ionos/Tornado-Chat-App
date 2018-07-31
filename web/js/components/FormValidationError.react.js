import React from 'react';


class FormValidationError extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            messages: props.messages
        };
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            messages: nextProps.messages
        });
    }

    render() {
        return (
            <div className="text-danger">
                {
                    this.state.messages.map((message, idx) => {
                        return <div key={"error-message-" + idx}>{message}</div>
                    })
                }
            </div>
        );
    }
}

export default FormValidationError;
