$(function () {
    url = new URL(window.location);

    // Calendar: set lines height to bars height:
    // SetTimeout(200) is required to be sure the js is fired after the css.
    // TODO: setTimeout(200) is a very dirty solution…
    let bars_height;
    setTimeout(function(){
        $('#calendar_retreats .calendar_bars').ready(function(){
        bars_height = $('#calendar_retreats .calendar_bars').css('height');
        $('#calendar_retreats .vertical_line').each(function () {
            $(this).css('height', bars_height);
        });
        });
    }, 200);
    setTimeout(function(){
        $('#calendar_sejours .calendar_bars').ready(function(){
        bars_height = $('#calendar_sejours .calendar_bars').css('height');
        $('#calendar_sejours .vertical_line').each(function () {
            $(this).css('height', bars_height);
        });
        });
    }, 200);
    setTimeout(function(){
        $('#calendar_parloirs .calendar_bars').ready(function(){
        bars_height = $('#calendar_parloirs .calendar_bars').css('height');
        $('#calendar_parloirs .vertical_line').each(function () {
            $(this).css('height', bars_height);
        });
        });
    }, 200);

    // Calendar: click on 'previous week':
    $('#previous_week').click(function () {
        const regex = /([^\/]*)\/(\d{2})\/(\d{2})\/(\d{4})/;
        const result = regex.exec(url);
        const date = new Date(parseInt(result[4]), parseInt(result[3]) - 1, parseInt(result[2]));
        const previous_date = new Date(date.getTime() - (7 * 24 * 3600 * 1000));

        let previous_day = previous_date.getDate();
        previous_day = previous_day < 10 ? '0' + previous_day : previous_day;

        let previous_month = previous_date.getMonth() + 1;
        previous_month = previous_month < 10 ? '0' + previous_month : previous_month;

        const previous_year = previous_date.getYear() + 1900;

        const page = result[1];
        window.location.href = '/hotellerie/' + page + '/' + previous_day + '/' + previous_month + '/' + previous_year;
    });


    // Calendar: click on 'next week':
    $('#next_week').click(function () {
        const regex = /([^\/]*)\/(\d{2})\/(\d{2})\/(\d{4})/;
        const result = regex.exec(url);
        const date = new Date(parseInt(result[4]), parseInt(result[3]) - 1, parseInt(result[2]));
        const next_date = new Date(date.getTime() + (7 * 24 * 3600 * 1000));

        let next_day = next_date.getDate();
        next_day = next_day < 10 ? '0' + next_day : next_day;

        let next_month = next_date.getMonth() + 1;
        next_month = next_month < 10 ? '0' + next_month : next_month;

        next_year = next_date.getYear() + 1900;

        const page = result[1];
        window.location.href = '/hotellerie/' + page + '/' + next_day + '/' + next_month + '/' + next_year;
    });


    // Calendar's datepicker:
    $('#datepicker').datetimepicker({
        format: 'L',
    });
    $('#datepicker').on('hide.datetimepicker', function (e) {
        const regex = /([^\/]*)\/\d{2}\/\d{2}\/\d{4}/;
        const result = regex.exec(url);
        const page = result[1];

        date = e.date._d;
        day = date.getDate();
        day = day < 10 ? '0' + day : day;
        month = date.getMonth() + 1;
        month = month < 10 ? '0' + month : month;
        year = date.getYear() + 1900;
        window.location.href = '/hotellerie/' + page + '/' + day + '/' + month + '/' + year;
    });


    // Sejours: has the personne a pere_suiveur?
    // On start (if we are on the right page,
    // elsewhere it raises an error on the server):
    if($('#id_mail_pere_suiveur').length){
        check_pere_suiveur();
    }
    // On change personne:
    $('#id_personne').change(function(){
        check_pere_suiveur();
    });


    // Sejours: manage rooms (checkboxes) and selects:
    // On start:
    refresh_rooms();
    // On modif datepickers:
    $('.sejour_date_row .datetimepicker-input').on({
        focusout: function(){
            if($('#id_sejour_au').val() == ''){
                $('#id_sejour_au').val($('#id_sejour_du').val());
            }
            refresh_rooms();
        },
    });
    // On modif repas (selects):
    $('.sejour_date_row select').on({
        change: function(){
            refresh_rooms();
        },
    });


    // Sejours: repas_au = repas_du if sejour_du = sejour_au:
    $('#id_repas_du').on({
        change: function(){
            if($('#id_sejour_au').val() == $('#id_sejour_du').val()){
                $('#id_repas_au').val($('#id_repas_du option:selected').val());
            }
            refresh_rooms();
        },
    });


    // Priests: manage appearence of concerned fields:
    // On start:
    priests_block_appearance();
    // On click on "priest with mass":
    $('#id_dit_messe').change(function(){
        priests_block_appearance();
    });
});


// ---------------------------------------------------------------------------------


function check_pere_suiveur(){
    const green = $('#id_personne').parent().find('label').css('color');
    personne = $('#id_personne option:selected').val();
    if(personne == ''){
        $('#id_mail_pere_suiveur').prop('disabled', true);
        $('#id_mail_pere_suiveur').parent().find('label').css('color', 'rgb(150, 150, 150)');
    }
    else{
        $.get(
            '/hotellerie/personnes/get_pere_suiveur/',
            {'personne': personne},
            function(back){
                $('#id_mail_pere_suiveur').prop('disabled', !(back['pere_suiveur'] && back['has_mail']));
                $('#id_mail_pere_suiveur').parent().find('label').css('color', (back['pere_suiveur'] && back['has_mail']) ? green : 'rgb(150, 150, 150)');
                if(back['pere_suiveur'] && back['has_mail']){
                    $('#id_mail_pere_suiveur').prop('checked', true);
                }
                else{
                    $('#id_mail_pere_suiveur').prop('checked', false);
                }
            },
            'json',
        );
    }
}


function refresh_rooms(){
    const param_sejour = url['pathname'].split('/')[3];
    const id_sejour = param_sejour != 'create' ? param_sejour : 0;
    const sejour_du = $('#id_sejour_du').val();
    const sejour_au = $('#id_sejour_au').val();
    const repas_du = $('#id_repas_du').val();
    const repas_au = $('#id_repas_au').val();
    const green = $('#id_chambre').parent().parent().find('label').css('color');
    if(sejour_du && sejour_au){
        $.get(
            '/hotellerie/sejours/rooms/', {
                'id_sejour': id_sejour,
                'start': sejour_du,
                'end': sejour_au,
                'repas_start': repas_du,
                'repas_end': repas_au,
            },
            function(back){
                for(i in back){
                    room = back[i];
                    const checkbox = $(`#id_chambre input[type=checkbox][value="${i}"]`);
                    if(room['occupied']){
                        checkbox.parent().css({'color': 'red'});
                        checkbox.parent().attr('title', room['title']);
                    }
                    else{
                        checkbox.parent().css({'color': green});
                        checkbox.parent().attr('title', '');
                    }
                }
            },
            'json',
        );
    }
}

function priests_block_appearance(){
    const green = $('#id_personne').parent().find('label').css('color');
    if($('#id_dit_messe').prop('checked')){
        $('#id_mail_sacristie').prop('checked', true);
    }
    else{
        $('#id_messe_premier_jour').prop('checked', false);
        $('#id_tour_messe').val('---------');
        $('#id_servant').prop('checked', false);
        $('#id_oratoire').val('---------');
        $('#id_mail_sacristie').prop('checked', false);
        $('#pretres').find('label').css('color', 'rgb(150, 150, 150)');
        $('#id_dit_messe').parent().find('label').css('color', green);
    }
    $('#id_messe_premier_jour').prop('disabled', !$('#id_dit_messe').prop('checked'));
    $('#id_tour_messe').prop('disabled', !$('#id_dit_messe').prop('checked'));
    $('#id_servant').prop('disabled', !$('#id_dit_messe').prop('checked'));
    $('#id_oratoire').prop('disabled', !$('#id_dit_messe').prop('checked'));
    $('#pretres').find('label').css('color', $('#id_dit_messe').prop('checked') ? green : 'rgb(150, 150, 150)');
    $('#id_dit_messe').parent().find('label').css('color', green);
    $('#id_mail_sacristie').prop('disabled', !$('#id_dit_messe').prop('checked'));
    $('#id_mail_sacristie').parent().find('label').css('color', $('#id_dit_messe').prop('checked') ? green : 'rgb(150, 150, 150)');
}