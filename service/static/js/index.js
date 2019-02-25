function categoryChange(e) {
    var good_a = ["spice", "crisp", "pepper", "cinnamon"];
    var good_b = ["fruit", "plum", "apple", "juici", "peach"];
    var good_c = ["acid", "tannin", "ripe", "lemon", "bitter"];
    var good_d = ["flower", "aroma"];
    var good_e = ["chocol", "almond", "caramel", "mocha", "vanilla", "creami", "coffee"];
    var good_f = ["citru", "herb", "orang", "grapefruit"];
    var good_g = ["wood", "smoki", "grapefruit"];
    var good_h = ["light", "soft", "smooth", "fresh"];
    var good_i = ["sweet", "honey"];
    var good_j = ["dri"];

    var target = document.getElementById("good");

    if (e.value == "a") var d = good_a;
    else if (e.value == "b") var d = good_b;
    else if (e.value == "c") var d = good_c;
    else if (e.value == "d") var d = good_d;
    else if (e.value == "e") var d = good_e;
    else if (e.value == "f") var d = good_f;
    else if (e.value == "g") var d = good_g;
    else if (e.value == "h") var d = good_h;
    else if (e.value == "i") var d = good_i;
    else if (e.value == "j") var d = good_j;

    target.options.length = 0;
    

    for (x in d) {
        var opt = document.createElement("option");
        opt.value = d[x];
        opt.innerHTML = d[x];
        target.appendChild(opt);
    }
}