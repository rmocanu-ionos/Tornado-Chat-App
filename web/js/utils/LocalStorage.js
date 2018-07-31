class LocalStorage {
    // patch the Storage object with utility methods
    static setObject(key, value) {
        localStorage.setItem(key, JSON.stringify(value));
    };

    static getObject(key) {
        let value = localStorage.getItem(key);
        return value && JSON.parse(value);
    };
}

export default LocalStorage;
