
  (function ($) {
  
  "use strict";

    // MENU
    $('.navbar-collapse a').on('click',function(){
      $(".navbar-collapse").collapse('hide');
    });
    
    // CUSTOM LINK
    $('.smoothscroll').click(function(){
      var el = $(this).attr('href');
      var elWrapped = $(el);
      var header_height = $('.navbar').height();
  
      scrollToDiv(elWrapped,header_height);
      return false;
  
      function scrollToDiv(element,navheight){
        var offset = element.offset();
        var offsetTop = offset.top;
        var totalScroll = offsetTop-navheight;
  
        $('body,html').animate({
        scrollTop: totalScroll
        }, 300);
      }
    });

    $(window).on('scroll', function(){
      function isScrollIntoView(elem, index) {
        var docViewTop = $(window).scrollTop();
        var docViewBottom = docViewTop + $(window).height();
        var elemTop = $(elem).offset().top;
        var elemBottom = elemTop + $(window).height()*.5;
        if(elemBottom <= docViewBottom && elemTop >= docViewTop) {
          $(elem).addClass('active');
        }
        if(!(elemBottom <= docViewBottom)) {
          $(elem).removeClass('active');
        }
        var MainTimelineContainer = $('#vertical-scrollable-timeline')[0];
        var MainTimelineContainerBottom = MainTimelineContainer.getBoundingClientRect().bottom - $(window).height()*.5;
        $(MainTimelineContainer).find('.inner').css('height',MainTimelineContainerBottom+'px');
      }
      var timeline = $('#vertical-scrollable-timeline li');
      Array.from(timeline).forEach(isScrollIntoView);

    const scrollText = document.getElementById("scroll-text");

      // 🌸 Your rotating messages
      const messages = [
        "Welcome to 文メイト — Learn Japanese with fun 🌸",
        "Master kanji, grammar, and writing with AI 💫",
        "Join your teacher and improve every day 📖",
        "Learn Japanese beautifully — anytime, anywhere 🗾"
      ];

      let currentIndex = 0;

      // Function to set message and restart animation
      function updateMessage() {
        // Stop current animation
        scrollText.style.animation = "none";

        // Update text content
        currentIndex = (currentIndex + 1) % messages.length;
        scrollText.textContent = messages[currentIndex];

        // Force reflow (restart animation)
        void scrollText.offsetWidth;

        // Restart animation
        scrollText.style.animation = "scrollLeft 25s linear infinite";
      }

      // Wait for one full scroll cycle before changing text
      setInterval(updateMessage, 25000); // match the CSS animation duration (25s)


    });
  })(window.jQuery);


