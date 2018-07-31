function login_func() {
    let data = document.getElementById("login_form").elements;
    let dict = {};
    dict["username"] = data.item(0).value;
    dict["password"] = data.item(1).value;

    let id = Math.floor(Math.random() * 100);
    let verb = "POST";
    let url = "/login";
    let body = dict;
    let headers = {};

    let obj = {
        "id": id,
        "verb": verb,
        "url": url,
        "body": body,
        "headers": headers
    }

    let ws = new WebSocket("ws://192.168.10.55:8887/ws");
    //ws.send(JSON.stringify(obj));
    ws.send("ssssss");


}