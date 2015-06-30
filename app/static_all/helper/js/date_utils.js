$.fn.default_datepicker = function() {
    this.datepicker({
        dateFormat: 'dd.mm.yy',
        dayNamesMin: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
        dayNamesShort: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
        monthNames: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
        monthNamesShort: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
        showOn: "both",
        // changeMonth: true,
        // changeYear: true,
        firstDay: 1,
        yearRange: "-100:+4",
        // buttonImage: "/static/project/img/calendar.png",
        // buttonImageOnly: true
    });
    return this;
};

$.fn.no_future_datepicker = function() {
    this.datepicker({
        dateFormat: 'dd.mm.yy',
        dayNamesMin: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
        dayNamesShort: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
        monthNames: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
        monthNamesShort: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
        // changeMonth: true,
        // changeYear: true,
        firstDay: 1,
        showOn: "both",
        // minDate: '0',
        maxDate: '0',
        yearRange: "-100:+4",
        // buttonImage: "/static/project/img/calendar.png",
        buttonImageOnly: true
    });
    return this;
};
