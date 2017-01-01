jQuery(function($) {

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

  function switch_theme() {
    var current_theme = $('link[title="main"]').attr('href');
    var current_index = themes.indexOf(current_theme);
    var next_index = current_index + 1;
    if (next_index >= themes.length) {
      next_index = 0;
    }
    set_theme(themes[next_index]);
  }

  if (supports_storage) {
    var theme = localStorage.theme;
    if (theme) {
      set_theme(theme);
    }
    $('#theme-switch').click(function() {
      switch_theme();
    });
  } else {
    $('#theme-switch').hide();
  }



});


