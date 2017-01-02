(function() {

  var themes = [
    '/css/bootstrap-serif.min.css',
    '/css/bootstrap-serif-dark.min.css'
  ];

  function supports_html5_storage() {
    try {
      return 'localStorage' in window && window['localStorage'] !== null;
    } catch (e) {
      return false;
    }
  }

  var supports_storage = supports_html5_storage();

  function set_theme(theme) {
    $('link[title="main"]').attr('href', theme);
    if (supports_storage) {
      localStorage.theme = theme;
    }
  }

  function set_font_size(size) {
    console.log('set_font_size: ' + size);
    $('p').css('font-size', parseInt(size));
    $('a.list-group-item').css('font-size', parseInt(size));
    if (supports_storage) {
      localStorage.fontSize = parseInt(size);
    }
  }

  function switch_theme() {
    var current_theme = $('link[title="main"]').attr('href');
    var current_index = themes.indexOf(current_theme);
    var next_index = current_index + 1;
    if (next_index >= themes.length) {
      next_index = 0;
    }
    set_theme(themes[next_index]);
    return false;
  }

  function increase_font_size() {
    var current_size = parseInt($('p').first().css('font-size'));
    if (current_size >= 200) {
      set_font_size(200);
    } else {
      set_font_size(current_size + 2);
    }
    return false;
  }

  function decrease_font_size() {
    var current_size = parseInt($('p').first().css('font-size'));
    if (current_size <= 8) {
      set_font_size(8);
    } else {
      set_font_size(current_size - 2);
    }
    return false;
  }

  $(function() {
    if (supports_storage) {

      var theme = localStorage.theme;
      if (theme) {
        set_theme(theme);
      }

      var fontSize = localStorage.fontSize;
      if (fontSize) {
        set_font_size(fontSize);
      }

      $('#theme-switch').click(switch_theme);
      $('#font-size-up').click(increase_font_size);
      $('#font-size-down').click(decrease_font_size);

    } else {

      $('#theme-buttons').hide();

    }
  });

}());
