$(document).ready(function() {

  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
  });

  $('#container').highcharts({
        data: {
            table: 'datatable'
        },
        chart: {
            type: 'column'
        },
        title: {
            text: 'Programs'
        },
        yAxis: {
            allowDecimals: false,
            title: {
                text: 'Units'
            }
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.name + '</b><br/>' +
                    this.point.y + ' ' + this.point.name.toLowerCase();
            }
        }
    });
  $('#container2').highcharts({
        data: {
            table: 'datatable'
        },
        chart: {
            type: 'spline'
        },
        title: {
            text: 'Programs'
        },
        yAxis: {
            allowDecimals: false,
            title: {
                text: 'Units'
            }
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.name + '</b><br/>' +
                    this.point.y + ' ' + this.point.name.toLowerCase();
            }
        }
    });
    $('#datatable').hide();
    // var $dataRows=$("#datatable2 tr");
    // var total = 0;
    // // console.log($dataRows.length);
    // $dataRows.each(function() {
    //             $(this).find('.avrg').each(function(i){
    //                 total+=parseInt( $(this).html());
    //             });
    //         });
    // var rapportage = document.getElementById("taux_rapportage");
    // rapportage.innerHTML = ""+ (total/ ($dataRows.length))*100 + "%";

});