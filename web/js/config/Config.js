// Define constants
class Config {

    constructor () {
        this.WS_URL = 'ws://' + location.hostname + ':' + location.port + '/ws/';
    }
}

let config = new Config();

export default config;
