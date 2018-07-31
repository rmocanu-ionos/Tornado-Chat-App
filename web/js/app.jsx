import React from 'react';
import { render } from 'react-dom'

import WebSocketConnection from './utils/WebSocketConnection';
import AviraMessenger from './components/AVMess.react';

let wsConnection = new WebSocketConnection();

// Render RaccoonApp Controller View
render(
    <AviraMessenger />,
    document.getElementById('avmess-app')
);
