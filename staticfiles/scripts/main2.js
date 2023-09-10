$(document).ready(function(){

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

/* document.addEventListener('DOMContentLoaded', {} => {
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    if ($navbarBurgers.length > 0){
        $navbarBurgers.forEach( el => {
            el.addEventListener('click', {} => {
                const target = el.dataset.target;
                const starget = document.getElementById(target);

                el.classList.toggle('is-active');
                starget.classList.toggle('is-active');
            });
        });
    }
}) */

    $('#register > form > .btn1').on(
        {mousedown: function(){
            $(this).css('-webkit-transform','scale(1.03)').css('-moz-transform','scale(1.03)').css('-o-transform','scale(1.03)');
        },
        mouseup: function(){
            $(this).css('-webkit-transform','scale(1)').css('-moz-transform','scale(1)').css('-o-transform','scale(1)');
        }}
    );
    function removeAllDropdowns(){
        $('.first').slideUp(500);
        $('.second').slideUp(500);
        /*
        $('#dropdown-account1').slideUp(500);
        $('#account-caret').hide();
        */
        /*
        $('.second #dropdown-shop').slideUp(500);
        $('.second #dropdown-deals').slideUp(500);
        $(".second #dropdown-brands").slideUp(500);
        $(".second #dropdown-services").slideUp(500);
        $('.second #dropdown-shop-caret > i').hide()
        $('.second #dropdown-deals-caret > i').hide()
        $('.second #dropdown-brands-caret > i').hide()
        $('.second #dropdown-services-caret > i').hide()
        */
    };
    function removeAccountDropdown(){
        $('.first').slideUp(500);
        /*
        $('#dropdown-account1').slideUp(500);
        $('#account-caret').hide();
        */
    };
    function removeNav3Dropdown(){
        $('.second').slideUp(500);
        /*
        $('.second #dropdown-shop').slideUp(500);
        $('.second #dropdown-deals').slideUp(500);
        $(".second #dropdown-brands").slideUp(500);
        $(".second #dropdown-services").slideUp(500);
        $('.second #dropdown-shop-caret > i').hide()
        $('.second #dropdown-deals-caret > i').hide()
        $('.second #dropdown-brands-caret > i').hide()
        $('.second #dropdown-services-caret > i').hide()
        */
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
        /*
        $('.second #dropdown-shop').css('margin-left','6.1%').css('border-radius','0 0 5px 5px').css('top','19.9vh');
        $('.second #dropdown-shop-caret > i').css('margin-left','7%').css('top','17.5vh');
        $('.second #dropdown-deals').css('margin-left','6.1%').css('border-radius','0 0 5px 5px').css('top','19.9vh');
        $('.second #dropdown-deals-caret > i').css('margin-left','13%').css('top','17.5vh');
        $('.second #dropdown-brands').css('margin-left','6.1%').css('border-radius','0 0 5px 5px').css('top','19.9vh');
        $('.second #dropdown-brands-caret > i').css('margin-left','19.5%').css('top','17.5vh');
        $('.second #dropdown-services').css('margin-left','6.1%').css('border-radius','0 0 5px 5px').css('top','19.9vh');
        $('.second #dropdown-services-caret > i').css('margin-left','25.4%').css('top','17.5vh');
        $('.second #dropdown-shop').css('display','none');
        $('.second #dropdown-deals').css('display','none');
        $(".second #dropdown-brands").css('display','none');
        $(".second #dropdown-services").css('display','none');
        $('.second #dropdown-shop-caret > i').css('display','none');
        $('.second #dropdown-deals-caret > i').css('display','none');
        $('.second #dropdown-brands-caret > i').css('display','none');
        $('.second #dropdown-services-caret > i').css('display','none');
        */
    };
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
            /*
            $('.second #dropdown-services').css('margin-left','6.1%').css('top','19.9vh');
            $('.second #dropdown-services-caret > i').css('margin-left','30%').css('top','17.5vh');
            */
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
            /*
            $('.second #dropdown-shop').css('margin-left','6.1%').css('top','24.9vh');
            $('.second #dropdown-deals').css('margin-left','6.1%').css('top','24.9vh');
            $('.second #dropdown-brands').css('margin-left','6.1%').css('top','24.9vh');
            $('.second #dropdown-services').css('margin-left','6.1%').css('top','24.9vh');

            $('.second #dropdown-shop-caret > i').css('margin-left','9.5%').css('top','22.5vh');
            $('.second #dropdown-deals-caret > i').css('margin-left','16.5%').css('top','22.5vh');
            $('.second #dropdown-brands-caret > i').css('margin-left','24.1%').css('top','22.5vh');
            $('.second #dropdown-services-caret > i').css('margin-left','30%').css('top','22.5vh');
            */
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

/*========================BASE HTML=================================*/
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

    $('#menubars').on(
        {mousedown: function(){
            $('#bars').css('display','none');
            $('#times').css('display','block');
            $("#dropdown-account2").animate({left:'0px'},1000);
            $('.first').hide();
            /*$('#dropdown-account1').hide()*/
        }}
    );
    $('#menutimes').on(
        {mousedown: function(){
            $('#bars').css('display','block');
            $('#times').css('display','none');
            $("#dropdown-account2").animate({left:'-300px'},1000);
            $('.first').hide();
        }}
    );
    $('#nav3 > .first-nav > ul li:first').on(
        {mouseenter: function(){
            displayNone()
            var x =currentScreen950
            window950(x)
            x.addListener(window950)
            /*
            $('#dropdown-shop-caret > i').css('display','block');
            $('#dropdown-shop').slideToggle(500);
            */
            $('.second > #dropdown-shop').css('display','block');
            $('.second').slideToggle(500);
        }}
    );
    $('#nav3 > .first-nav > ul li:nth(1)').on(
        {mouseenter: function(){
            displayNone()
            var x =currentScreen950
            window950(x)
            x.addListener(window950)
            /*
            $('#dropdown-deals-caret > i').css('display','block');
            $("#dropdown-deals").slideToggle(500);
            */
            $('.second > #dropdown-deals').css('display','block');
            $('.second').slideToggle(500);
        }}
    );
    $('#nav3 > .first-nav > ul li:nth(2)').on(
        {mouseenter: function(){
            displayNone()
            var x =currentScreen950
            window950(x)
            x.addListener(window950)
            /*
            $('#dropdown-brands-caret > i').css('display','block');
            $("#dropdown-brands").slideToggle(500);
            */
            $('.second > #dropdown-brands').css('display','block');
            $('.second').slideToggle(500);
        }}
    );
    $('#nav3 > .first-nav > ul li:nth(3)').on(
        {mouseenter: function(){
            displayNone()
            var x =currentScreen1100
            window1100(x)
            x.addListener(window1100)
            var x =currentScreen950
            window950(x)
            x.addListener(window950)
            /*
            $("#dropdown-services-caret > i").css('display','block');
            $("#dropdown-services").slideToggle(500);
            */
            $('.second > #dropdown-services').css('display','block');
            $('.second').slideToggle(500);
        }}
    );
    $('#nav1 > .main-nav > .inside > a > .account').on(
        {mouseenter: function(){
            $('.first').slideToggle(500);
            /*$('#dropdown-account1').slideToggle(500);
            $('#account-caret').show();*/
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
            /*$('#dropdown-account1').slideUp(500);
            $('#account-caret').hide();*/
            $('#nav1 > .main-nav > .inside > a > .cart > i').css("color","var(--normalorange)");
            $('#nav1 > .main-nav > .inside > a > .cart > #qty').css("color","var(--normalorange)");
            $('#nav1 > .main-nav > .inside > a > .cart > .text').css("color","var(--normalorange)");
        },
        mouseleave: function(){
            $('#nav1 > .main-nav > .inside > a > .cart > i').css("color","var(--normalwhite)");
            $('#nav1 > .main-nav > .inside > a > .cart > #qty').css("color","var(--normalblack)");
            $('#nav1 > .main-nav > .inside > a > .cart > .text').css("color","var(--normalwhite)");
        }}
    );
    $('#nav1 > .main-nav > .inside > a > .store').on(
        {mouseenter: function(){
            $('.first').slideUp(500);
            /*$('#dropdown-account1').slideUp(500);
            $('#account-caret').hide();*/
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

    $('#dropdown-account1').on(
        {mouseenter: function(){
            $('.first').show();
            /*$('#dropdown-account1').show();
            $('#account-caret').show();*/
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
    /*$('#nav1 > .main-nav > .account').on(
        {mouseleave: function(){
            if (myFunction().showing == true){
                $('#dropdown-account1').show();
            } else {
                $('#dropdown-account1').hide();
            }
        }}
    );*/

    $('#section-container').on(
        {mouseenter: function(){
            $('.first').slideUp(500);
            /*$('#dropdown-account1').slideUp(500);
            $('#account-caret').hide();*/
            $('#dropdown-shop').slideUp(500);
            $('#dropdown-deals').slideUp(500);
            $("#dropdown-brands").slideUp(500);
            $("#dropdown-services").slideUp(500);
            $('#dropdown-shop-caret > i').hide()
            $('#dropdown-deals-caret > i').hide()
            $('#dropdown-brands-caret > i').hide()
            $('#dropdown-services-caret > i').hide()
        },
        mousedown: function(){
        }}
    );
    $('#dropdown-categories').on(
        {mouseenter: function(){
            $('.first').slideToggle(500);
            /*$('#dropdown-account1').slideToggle()*/
            $('#dropdown-account2').hide()
        },
        mousedown: function(){
            $('.first').slideToggle(500);
            /*$('#dropdown-account1').slideToggle()*/
            $('#dropdown-account2').hide()
        }}
    );

/*===========================FRONTPAGE HTML==============================*/



});