import React from 'react';
import { Link } from 'react-router';


class TopBar extends React.Component {

    render() {
        return (
            <div>
            <nav className="navbar navbar-default" role="navigation" style={{marginBottom: '0px'}}>
                <div className="container">
                    <div className="navbar-header">
                        <Link className="navbar-brand" to="/">Avira Messenger</Link>
                    </div>
                    <ul className="nav navbar-nav">
                        <li>
                            <Link to="login">Login</Link>
                        </li>
                        <li>
                            <Link to="register">Register</Link>
                        </li>
                    </ul>
                </div>
            </nav>
            </div>
        );
    }
}

export default TopBar;
