$(function () {

  var QueryString = (function(a) {
    if (a == "") return {};
    var b = {};
    for (var i = 0; i < a.length; ++i) {
      var p=a[i].split('=', 2);
      if (p.length == 1)
        b[p[0]] = "";
      else
        b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
    }
    return b;
  })(window.location.search.substr(1).split('&'));

  var SERVER_DEFAULT = 'http://localhost:8032'
  var server = QueryString.server || SERVER_DEFAULT;

  $.get(server + '/list', function (data) {
    var list = null, taskName = null;
    data.filenames.forEach(function (x) {
      var tokens = x.split('_');
      if (tokens[0] != taskName) {
        $('<h1>').text(tokens[0]).appendTo('#file-column');
        taskName = tokens[0];
        list = $('<ul>').appendTo('#file-column');
      }
      $('<li>').text(tokens[1]).appendTo(list).data('filename', x);
    });
  });

  var currentFile = null;

  $('#file-column').on('click', 'li', function (event) {
    var target = $(this);
    $('#file-column li').removeClass('selected');
    $(target).addClass('selected');
    currentFile = target.data('filename');
    $.get(server + '/view', {'filename': currentFile}, function (data) {
      if (data.filename !== currentFile) return;    // Stale
      //console.log(data);
      $('#display-metadata').empty();
      var metadataTable = $('<table class=metadata>').appendTo('#display-metadata');
      addToTable(metadataTable, 'filename', data.filename);
      var episode = data.episode;
      addToTable(metadataTable, 'task', episode.taskName);
      var config;
      if (/flight\..*/.test(episode.taskName)) {
        config = {width: 376, height: 668, scale: 1.0};
      }
      addToTable(metadataTable, 'reward', Math.round(episode.reward * 100) / 100);
      addToTable(metadataTable, 'raw reward', episode.rawReward);
      if (episode.rawReward > 0) {
        $('#display-metadata')[0].className = 'success';
      } else {
        $('#display-metadata')[0].className = 'fail';
      }
      addToTable(metadataTable, 'utterance', episode.utterance);
      if (typeof episode.fields !== 'undefined')
        addToTable(metadataTable, 'fields', JSON.stringify(episode.fields));
      if (episode.states[0].image) {
        addToTable(metadataTable, '', '<b>Images available! Hold Z to view.</b>', true);
      }
      $('#display-episode').empty().scrollTop(0);
      episode.states.forEach(function (state, i) {
        $('#display-episode').append(drawState(state, config));
      });
    });
  });

  // Helper functions
  function addToTable(table, key, value, raw) {
    return $('<tr>')
      .append($('<th>').text(key))
      .append($('<td>')[raw ? 'append' : 'text'](value))
      .appendTo(table);
  }

  function drawState(data, config) {
    config = config || {width: 241, height: 316, scale: 1.5};
    var wrapper = $('<div class=state-wrapper>');
    var metadataTable = $('<table class=metadata>').appendTo(wrapper);
    addToTable(metadataTable, 'time', Math.round(data.time / 10) / 100);
    addToTable(metadataTable, 'action', data.action ? data.action.type : 'n/a');
    addToTable(metadataTable, 'timing', data.action ?
        (data.action.timing == 1 ? 'BEFORE' :
         data.action.timing == 3 ? 'AFTER' : data.action.timing) : 'n/a');
    var screenWrapper = $('<div class=screen-wrapper>').appendTo(wrapper);
    var canvas = $('<canvas width=' + config.width +
        ' height=' + config.height + '>').appendTo(screenWrapper);
    var ctx = canvas[0].getContext('2d');
    ctx.scale(config.scale, config.scale);
    var recordingTarget = drawDOM(data.dom, ctx);
    addToTable(metadataTable, 'target', recordingTarget ? recordingTarget.tag : "(none)");
    addToTable(metadataTable, '',
        $('<button>').text('DUMP').click(function () {console.log(data);}), true);
    if (data.action) {
      drawAction(data.action, ctx);
    }
    if (data.image) {
      $('<img>').attr('src', data.image).appendTo(screenWrapper);
    }
    return wrapper;
  }

  // Returns the recordingTarget or null
  function drawDOM(data, ctx) {
    ctx.fillStyle = data.recordingTarget ? '#DDF' : 'white';
    ctx.fillRect(data.left, data.top, data.width, data.height);
    ctx.strokeStyle = data.focused ? 'red' : 'black';
    ctx.strokeRect(data.left, data.top, data.width, data.height);
    if (data.text) {
      ctx.fillStyle = (data.tag == 't') ? 'lightgray' : 'black';
      ctx.textBaseline = 'top';
      ctx.fillText(data.text, data.left, data.top);
    }
    if (data.value) {
      ctx.fillStyle = 'green';
      ctx.textBaseline = 'top';
      ctx.fillText(data.value, data.left, data.top);
    }
    var recordingTarget = data.recordingTarget ? data : null;
    data.children.forEach(function (child) {
      var childIsRecordingTarget = drawDOM(child, ctx);
      recordingTarget = recordingTarget || childIsRecordingTarget;
    });
    return recordingTarget;
  }

  function drawAction(action, ctx) {
    //console.log(action);
    var t = action.type
    if (t == 'click' || t == 'dblclick' || t == 'mousedown' || t == 'mouseup') {
      ctx.beginPath();
      ctx.arc(
          (action.cx !== undefined ? action.cx : action.x),
          (action.cy !== undefined ? action.cy : action.y), 5, 0,2*Math.PI);
      ctx.fillStyle = {'click': 'blue', 'dblclick': 'orange',
        'mousedown': 'green', 'mouseup': 'red'}[t];
      ctx.fill();
    } else if (t == 'keypress' || t == 'keydown' || t == 'keyup') {
      ctx.fillStyle = {'keypress': 'blue', 'keydown': 'green', 'keyup': 'red'}[t];
      ctx.textBaseline = 'top';
      ctx.fillText(t + ': key=' + action.keyCode + ' char=' + action.charCode, 0, 0);
    } else if (t == 'scroll') {
    }
  }

  $(document).keydown(function (event) {
    console.log(event);
    if (event.keyCode == 90) {    // Z
      $('#display-column').addClass('show-images');
    }
  });
  $(document).keyup(function (event) {
    if (event.keyCode == 90) {    // Z
      $('#display-column').removeClass('show-images');
    }
  });

});
