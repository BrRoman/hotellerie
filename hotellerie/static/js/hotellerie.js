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


    // Sejours: room's status:
    $('.sejour_date_row .datetimepicker-input').on({
        focusout: function(){
            refresh_rooms();
        },
    });
    $('.sejour_date_row select').on({
        change: function(){
            refresh_rooms();
        },
    });
});

function refresh_rooms(){
    $.get(
        '/hotellerie/sejours/rooms/',
        {'start': 1,
        'end': 2},
        function(back){
            console.log(back);
        },
        'json',
    );
}