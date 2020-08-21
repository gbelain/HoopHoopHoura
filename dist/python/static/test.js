$(function () {
    $("#UID_boutonTest").click(function () {
        $.getJSON(
            "/_add_numbers",
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
