$(document).ready(function () {
    url = new URL(window.location);

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


    // Sejours: manage rooms (checkboxes):
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
            if($('#id_repas_au option:selected').val() == '---------'){
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

function refresh_rooms(){
    const param_sejour = url['pathname'].split('/')[3];
    const id_sejour = param_sejour != 'create' ? param_sejour : 0;
    const sejour_du = $('#id_sejour_du').val();
    const sejour_au = $('#id_sejour_au').val();
    const repas_du = $('#id_repas_du').val();
    const repas_au = $('#id_repas_au').val();
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
                    if(room['occupied']){
                        const checkbox = $(`#id_chambre input[type=checkbox][value="${i}"]`);
                        checkbox.parent().css({'color': 'red'});
                        checkbox.parent().attr('title', room['title']);
                    }
                }
            },
            'json',
        );
    }
}

function priests_block_appearance(){
    const green = $('#id_dit_messe').parent().find('label').css('color');
    if(!$('#id_dit_messe').prop('checked')){
        $('#id_messe_lendemain').prop('checked',  false);
        $('#id_tour_messe').val('---------');
        $('#id_servant').prop('checked',  false);
        $('#pretres').find('label').css('color', 'rgb(150, 150, 150)');
        $('#id_dit_messe').parent().find('label').css('color', green);
    }
    $('#id_messe_lendemain').prop('disabled', !$('#id_dit_messe').prop('checked'));
    $('#id_tour_messe').prop('disabled', !$('#id_dit_messe').prop('checked'));
    $('#id_servant').prop('disabled', !$('#id_dit_messe').prop('checked'));
    $('#pretres').find('label').css('color', $('#id_dit_messe').prop('checked') ? green : 'rgb(150, 150, 150)');
    $('#id_dit_messe').parent().find('label').css('color', green);
}