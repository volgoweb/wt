$.fn.default_datepicker = function() {
    this.datetimepicker({
        lang:'ru',
        i18n:{
         ru:{
          months:[
           'Январь','Февраль','Март','Апрель',
           'Май','Июнь','Июль','Август',
           'Сентябрь','Октябрь','Ноябрь','Декабрь',
          ],
          dayOfWeek:[
           "Вс", "Пн", "Вт", "Ср", 
           "Чт", "Пт", "Сб",
          ]
         }
        },
        timepicker:false,
        format:'d.m.Y',
        allowBlank: true,
        dayOfWeekStart: 1,
        defaultSelect: false,
    });
    return this;
};

$.fn.default_datetimepicker = function() {
    this.datetimepicker({
        lang:'ru',
        i18n:{
         ru:{
          months:[
           'Январь','Февраль','Март','Апрель',
           'Май','Июнь','Июль','Август',
           'Сентябрь','Октябрь','Ноябрь','Декабрь',
          ],
          dayOfWeek:[
           "Вс", "Пн", "Вт", "Ср", 
           "Чт", "Пт", "Сб",
          ]
         }
        },
        format:'d.m.Y H:i',
        step: 30,
        allowBlank: true,
        dayOfWeekStart: 1,
        defaultSelect: false,
    });
    return this;
};
