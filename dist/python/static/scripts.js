$(function () {
    $("#UID_boutonTest").click(function () {
        $.getJSON(
            "/_process_video",
            {
                a: document.getElementById("aInput").value,
                b: document.getElementById("bInput").value,
            },
            function (data) {
                $("#UID_afficheTest").text(data.result);
            }
        );
        return false;
    });
});

(function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
                this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top - 72,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $("body").scrollspy({
        target: "#mainNav",
        offset: 74,
    });

    // Collapse Navbar
    var navbarCollapse = function () {
        if ($("#mainNav").offset().top > 100) {
            $("#mainNav").addClass("navbar-shrink");
        } else {
            $("#mainNav").removeClass("navbar-shrink");
        }
    };
    // Collapse now if page is not at top
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);
})(jQuery); // End of use strict

("use strict");
window.addEventListener("load", async (e) => {
    if ("serviceWorker" in navigator) {
        try {
            navigator.serviceWorker.register("sw.js");
            console.log("SW registered");
        } catch (error) {
            console.log("SW registration failed");
        }
    }
});

/******************************************************************************** */

function runscript() {
    alert("j'aimerais que ça marche putain!");
    // if (document.getElementById("script_run").innerHTML == "ONLINE") {
    //     $.ajax({
    //         type: "POST",
    //         url: "main.py",
    //         data: { offline: "True" },
    //     }).done(
    //         setTimeout(function () {
    //             changebutton();
    //         }, 50000)
    //     );
    // } else {
    //     $.ajax({
    //         url: "main.py",
    //     }).done(
    //         setTimeout(function () {
    //             changebutton();
    //         }, 50000)
    //     );
    // }
}
