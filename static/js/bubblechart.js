
var context_menu = document.getElementById('context-menu');
function show_context_menu(x, y, status_id) {
    context_menu.style.visibility = 'visible';
    context_menu.innerHTML = status_html(status_id_lut[status_id]);
}

function update_chart() {

    var x = [], y = [], s = [], t = [];
    for (var i = 0; i < statuses.length; i++) {
        var status = statuses[i];
        if (status.followers_count < 1000 || status['retweet_count'] + status['favorite_count'] < 10)
            continue;
        x.push(new Date(status['created_at']));
        y.push(status['retweet_count'] + status['favorite_count']);
        s.push(5 + 0.005 * Math.sqrt(status.followers_count));
        t.push(status['id']);
    }

    var data = [{ x: x, y: y, text: t, mode: 'markers', marker: { size: s, } }];

    tz_offset = moment.tz(moment.tz.guess()).format('Z z')

    var layout = {
        showlegend: false,
        height: 400,
        width: 1200,
        hovermode: 'closest',
        yaxis: { 
            type: 'log', 
            title: { text: 'Retweets + Favorites', },
            // fixedrange: true 
        },
        xaxis: { 
            title: { text: `Time ${tz_offset}`, }, 
            // rangeselector: {},
            // rangeslider: {},
            // fixedrange: true
        },
        margin: {
          l: 65,
          r: 0,
          b: 75,
          t: 10,
          pad: 4
        },
    };

    var myPlot = document.getElementById('bubblechart');
    Plotly.newPlot('bubblechart', data, layout);
    myPlot.on('plotly_click', function(data) {
        event = data.event;
        point = data.points[0];
        show_context_menu(event.pageX, event.pageY, point.text);
    });
    /*.on('plotly_unhover', function(data) {
        hide_context_menu();
    });*/

}

function get_status(status_id) {
    return status_id_lut[status_id];
}

function get_status_html(status_id) {
    var status = get_status(status_id);
    return `<div class="status">
        <img class="thumb" data-src="${status.profile_image_url_https}">
        <div class="meta">
        <span class="name">${status.name}</span> &nbsp;
        <span class="screen_name">
        <a href="https://twitter.com/${status.screen_name}" target="_blank">@${status.screen_name}</a></span> &nbsp;
        <span class="social">${numbers_with_commas(status.followers_count)} followers</span>
        <span class="time">
            <i class="far fa-retweet"></i> <strong>${numbers_with_commas(status.retweet_count)}</strong> 
            <i class="far fa-heart"></i> <strong>${numbers_with_commas(status.favorite_count)}</strong> &nbsp;&nbsp; 
            ${status.created_at}</span>
        </div>
        <div class="content">
        <div class="text">${urlify(status.text)}</div>
        </div>`;
}