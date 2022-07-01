const tmp = `
历史消息（查看新消息请手动刷新）
<div id="chatdata"></div>
<span class="btn" id="morehistory">加载更多</span><br>
<script src="{{ url_for('static', filename = 'admin_script.js') }}" defer async></script>`
document.getElementById('admin').innerHTML = tmp;
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
    fetch('/api?t=' + (lasttimestamp == -1 ? Date.now() : lasttimestamp) + '&c=' + more + '&a=1').then(res => res.json()).then(data => {
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
document.getElementById('morehistory').click();