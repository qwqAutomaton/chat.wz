let clickable = true;
let lasttimestamp = -1;
document.getElementById('morehistory').addEventListener('click', function (e) {
    if (!clickable) return;
    function appendMessage(text, ele) {
        let p = document.createElement('p');
        let t = document.createTextNode(text);
        p.appendChild(t);
        ele.appendChild(p);
    }
    let datadiv = document.getElementById('chatdata');
    let more = 5;
    let that = this;
    that.innerText = 'Loading...';
    fetch('/api?t=' + (lasttimestamp == -1 ? Date.now() : lasttimestamp) + '&c=' + more).then(res => res.json()).then(data => {
        let content = data.content;
        if (content.length == 0) {
            that.innerText = '--空的--';
            clickable = false;
            that.className = '';
            return;
        }
        for (let i in content) {
            let val = content[i];
            let msg = val[4];
            let nick = val[2];
            let time = val[3];
            appendMessage(nick + '@' + (new Date(time)).toLocaleString() + ':' + msg, datadiv);
        }
        let tmp = content.pop();
        tmp.pop();
        lasttimestamp = tmp.pop() - 1;
        if (data.tail) {
            that.innerText = '--没了--';
            clickable = false;
            that.className = '';
        } else {
            that.innerText = '加载更多';
            clickable = true;
        }
    });
})
let sendAvaliable = true;
document.getElementById('submit').addEventListener('click', function (e) {
    let content = document.getElementById('content').value;
    let nickname = document.getElementById('nickname').value;
    if (content == '') { alert('不可发送空消息。'); return; }
    if (nickname == '') nickname = '匿名';
    let timestamp = Date.now();
    document.getElementById('content').value = '';
    sendAvaliable = false;
    fetch('/api', {
        method: 'post',
        body: JSON.stringify({ n: nickname, t: timestamp, c: content }),
        headers: {
            'Content-Type': 'application/json; charset=utf-8'
        }
    }).then(data => {
        if (data.json().code == -1) alert('错误：发送失败。');
        console.log(data);
        window.location.replace('/');
    })
});
document.getElementById('morehistory').click();