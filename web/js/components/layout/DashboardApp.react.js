import React from 'react';

import TopBar from './TopBar.react';


class DashboardApp extends React.Component {

    constructor(props, context) {
        super(props, context);
    }

    render() {
        return (
            <div className="container-fluid">
                <div className="row">
                    <TopBar />
                </div>
                <div className="container">
                    {this.props.children}
                </div>
            </div>
        );
    }
}

export default DashboardApp;
