

$(document).ready(function(){
    function window1200(currentScreen){
        if (currentScreen.matches){
        };
    }
    function window1150(currentScreen){
        if (currentScreen.matches){
        };
    }
    function window1100(currentScreen){
        if (currentScreen.matches){
        };
    }
    function window1050(currentScreen){
        if (currentScreen.matches){
        };
    }
    function window1000(currentScreen){
        if (currentScreen.matches){
        };
    }
    function window950(currentScreen){
        if (currentScreen.matches){
            $('.second').css('margin-left','6.1%').css('top','22vh')
        };
    }
    function window900(currentScreen){
        if (currentScreen.matches){
        };
    }
    function window850(currentScreen){
        if (currentScreen.matches){
        };
    }
    function window800(currentScreen){
        if (currentScreen.matches){
        };
    }
    function window768(currentScreen){
        if (currentScreen.matches){
        };
    }
    function window320(currentScreen){
        if (currentScreen.matches){
        };
    }
    /*max-width:1200px=darkgrey*/
    /*max-width:1100px=color:pink*/
    /*max-width:1050px=color:black*/
    /*max-width:950px=green*/
    /*max-width:900px=darkgrey*/
    /*max-width:850px=normalorange*/
    /*max-width:800px=color:red*/
    var currentScreen1200 = window.matchMedia("(max-width:1200px)")
    var currentScreen1150 = window.matchMedia("(max-width:1150px)")
    var currentScreen1100 = window.matchMedia("(max-width:1100px)")
    var currentScreen1050 = window.matchMedia("(max-width:1050px)")
    var currentScreen1000 = window.matchMedia("(max-width:1000px)")
    var currentScreen950 = window.matchMedia("(max-width:950px)")
    var currentScreen900 = window.matchMedia("(max-width:900px)")
    var currentScreen850 = window.matchMedia("(max-width:850px)")
    var currentScreen800 = window.matchMedia("(max-width:800px)")
    var currentScreen768 = window.matchMedia("(max-width:768px)")
    var currentScreen320 = window.matchMedia("(max-width:320px)")
    function removeAllDropdowns(){
        $('.first').slideUp(500);
        $('.second').slideUp(500);
    };
    function removeAccountDropdown(){
        $('.first').slideUp(500);
    };
    function removeNav3Dropdown(){
        $('.second').slideUp(500);
    };
    function displayNone(){
        $('.second').css('margin-left','6.1%').css('top','17vh')

        $('.second > #dropdown-shop > .caret').css('margin-left','2%').css('top','-0.2vh');
        $('.second > #dropdown-shop > ul').css('top','3vh');
        $('.second > #dropdown-deals > .caret').css('margin-left','16%').css('top','-0.2vh');
        $('.second > #dropdown-deals > ul').css('top','3vh');
        $('.second > #dropdown-brands > .caret').css('margin-left','31%').css('top','-0.2vh');
        $('.second > #dropdown-brands > ul').css('top','3vh');
        $('.second > #dropdown-services > .caret').css('margin-left','49%').css('top','-0.2vh');
        $('.second > #dropdown-services > ul').css('top','3vh');

        $('.second').css('display','none');
        $('.second > #dropdown-shop').css('display','none');
        $('.second > #dropdown-deals').css('display','none');
        $('.second > #dropdown-brands').css('display','none');
        $('.second > #dropdown-services').css('display','none');
    };
/*========================BASE HTML=================================*/
    $('#menubars').on(
        {mousedown: function(){
            $('#menubars').css('display','none');
            $('#menutimes').css('display','block');
            $(".third").animate({left:'0'},1000);
            $('.first').hide();
        }}
    );

    $('#menutimes').on(
        {mousedown: function(){
            $('#menubars').css('display','block');
            $('#menutimes').css('display','none');
            $(".third").animate({left:'-300px'},1000);
            $('.first').hide();
        }}
    );
    $('#menutimes2').on(
        {mousedown: function(){
            $('#menubars').css('display','block');
            $('#menutimes').css('display','none');
            $(".third").animate({left:'-300px'},1000);
            $('.first').hide();
        }}
    );
    $('#nav3 > .first-nav > ul li:first').on(
        {mouseenter: function(){
            displayNone()
            var x =currentScreen950
            window950(x)
            x.addEventListener(window950)
            $('.second > #dropdown-shop').css('display','block');
            $('.second').slideToggle(500);
        }}
    );
    $('#nav3 > .first-nav > ul li:nth(1)').on(
        {mouseenter: function(){
            displayNone()
            var x =currentScreen950
            window950(x)
            x.addEventListener(window950)
            $('.second > #dropdown-deals').css('display','block');
            $('.second').slideToggle(500);
        }}
    );
    $('#nav3 > .first-nav > ul li:nth(2)').on(
        {mouseenter: function(){
            displayNone()
            var x =currentScreen950
            window950(x)
            x.addEventListener(window950)
            $('.second > #dropdown-brands').css('display','block');
            $('.second').slideToggle(500);
        }}
    );
    $('#nav3 > .first-nav > ul li:nth(3)').on(
        {mouseenter: function(){
            displayNone()
            var x =currentScreen1100
            window1100(x)
            x.addEventListener(window1100)
            var x =currentScreen950
            window950(x)
            x.addEventListener(window950)
            $('.second > #dropdown-services').css('display','block');
            $('.second').slideToggle(500);
        }}
    );
    $('#nav1 > .main-nav > .inside > a > .account').on(
        {mouseenter: function(){
            $('.first').slideToggle(500);
            $('#nav1 > .main-nav > .inside > a > .account > i').css("color","var(--normalorange)");
            $('#nav1 > .main-nav > .inside > a > .account > #caret4').css("color","var(--normalorange)");
            $('#nav1 > .main-nav > .inside > a > .account > .text').css("color","var(--normalorange)");
        },
        mouseleave: function(){
            $('#nav1 > .main-nav > .inside > a > .account > i').css("color","var(--normalwhite)");
            $('#nav1 > .main-nav > .inside > a > .account > #caret4').css("color","var(--normalwhite)");
            $('#nav1 > .main-nav > .inside > a > .account > .text').css("color","var(--normalwhite)");
        }}
    );
    $('#nav1 > .main-nav > .inside > a > .cart').on(
        {mouseenter: function(){
            $('.first').slideUp(500);
            $('#nav1 > .main-nav > .inside > a > .cart > i').css("color","var(--normalorange)");
            $('#nav1 > .main-nav > .inside > a > .cart > .qty').css("color","var(--normalorange)");
            $('#nav1 > .main-nav > .inside > a > .cart > .text').css("color","var(--normalorange)");
        },
        mouseleave: function(){
            $('#nav1 > .main-nav > .inside > a > .cart > i').css("color","var(--normalwhite)");
            $('#nav1 > .main-nav > .inside > a > .cart > .qty').css("color","var(--normalblack)");
            $('#nav1 > .main-nav > .inside > a > .cart > .text').css("color","var(--normalwhite)");
        }}
    );
    $('#nav1 > .main-nav > .inside > a > .store').on(
        {mouseenter: function(){
            $('.first').slideUp(500);
            $('#nav1 > .main-nav > .inside > a > .store > i').css("color","var(--normalorange)");
            $('#nav1 > .main-nav > .inside > a > .store > #caret3').css("color","var(--normalorange)");
            $('#nav1 > .main-nav > .inside > a > .store > .text').css("color","var(--normalorange)");
        },
        mouseleave: function(){
            $('#nav1 > .main-nav > .inside > a > .store > i').css("color","var(--normalwhite)");
            $('#nav1 > .main-nav > .inside > a > .store > #caret3').css("color","var(--normalwhite)");
            $('#nav1 > .main-nav > .inside > a > .store > .text').css("color","var(--normalwhite)");
        }}
    );
    $('#nav4 > .main-nav > a > .cart').on(
        {mouseenter: function(){
            $('.first').slideUp(500);
            $('#nav4 > .main-nav > a > .cart > i').css("color","var(--normalorange)");
            $('#nav4 > .main-nav > a > .cart > .qty').css("color","var(--normalorange)");
            $('#nav4 > .main-nav > a > .cart > .text').css("color","var(--normalorange)");
        },
        mouseleave: function(){
            $('#nav4 > .main-nav > a > .cart > i').css("color","var(--normalwhite)");
            $('#nav4 > .main-nav > a > .cart > .qty').css("color","var(--normalblack)");
            $('#nav4 > .main-nav > a > .cart > .text').css("color","var(--normalwhite)");
        }}
    );

    $('#dropdown-account1').on(
        {mouseenter: function(){
            $('.first').show();
        }}
    );

    $('#nav1').on(
        {mouseenter: function(){
            removeNav3Dropdown()
        }}
    );
    $('#nav1 > .main-nav > .store').on(
        {mouseenter: function(){
            removeAccountDropdown()
        }}
    );
    $('#nav1 > .main-nav > .cart').on(
        {mouseenter: function(){
            removeAccountDropdown()
        }}
    );
    $('#nav2').on(
        {mouseenter: function(){
            removeAllDropdowns()
        }}
    );
    $('#nav3 > .first-nav').on(
        {mouseenter: function(){
            removeAccountDropdown()
        }}
    );
    $('#nav3 > .main-nav').on(
        {mouseenter: function(){
            removeNav3Dropdown()
        }}
    );
    $('#section-container').on(
        {mouseenter: function(){
            $('.first').slideUp(500);
            $('.second').slideUp(500);
        },
        mousedown: function(){
            $(".third").animate({left:'-300px'},1000);
            if (window.matchMedia("(max-width:768px)").matches){
                $('#menutimes').css('display','none');
                $('#menubars').css('display','block');
            };
        }}
    );

/*===========================OTHERS==============================*/

    $('#account-navbar1').on(
        {click: function(e){
            e.preventDefault();
            $('#account-navbar2').toggle(5000)
        }}
    )

    $('.search-box .side .brand form .list .items').on(
        {mousedown: function(){
            $(this).text('border');

        }}
    );

    $('.side .brand form .search-field .field input').on(
        {mousedown: function(){
            $(this).css('border','none');
        },
        mouseup: function(){
            $(this).css('border','0.1px solid #ACADA8');
        }}
    );

    $('#register > form > .btn1').on(
        {mousedown: function(){
            $(this).css('-webkit-transform','scale(1.03)').css('-moz-transform','scale(1.03)').css('-o-transform','scale(1.03)');
        },
        mouseup: function(){
            $(this).css('-webkit-transform','scale(1)').css('-moz-transform','scale(1)').css('-o-transform','scale(1)');
        }}
    );


});