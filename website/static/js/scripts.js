var citiesOptions = {
    url: "/api/public/cities.json",
    getValue: "name",
    list: {
        match: {
            enabled: true
        }
    },
    theme: "square"
};

$("#user_settings #id_city").easyAutocomplete(citiesOptions);

var skillsOptions = {
    url: "/api/public/skills.json",
    getValue: "name",
    list: {
        match: {
            enabled: true
        }
    },
    theme: "square"
};

$("#skill_form #id_skill").easyAutocomplete(skillsOptions);
$("#need_form #id_skill").easyAutocomplete(skillsOptions);

$(document).on('click', 'a.skill-deleter', function (e) {
    if(!confirm(LANG_ARE_YOUR_SURE_YOU_WANT_TO_DELETE_THIS_SKILL)) {
        e.preventDefault();
    }
});

$(document).on('click', 'a.need-deleter', function (e) {
    if(!confirm(LANG_ARE_YOUR_SURE_YOU_WANT_TO_DELETE_THIS_NEED)) {
        e.preventDefault();
    }
});