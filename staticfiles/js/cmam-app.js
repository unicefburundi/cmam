// sorting json
function sortObject(o) {
    return Object.keys(o).sort().reduce((r, k) => (r[k] = o[k], r), {});
}

// sum of jsons
function getsum(response){
    var weeks = {},
        columns = {},
        sumCols = ['total_debut_semaine','ptb', 'oedemes', 'rechute', 'readmission', 'transfert_interne_i','gueri', 'deces', 'abandon', 'non_repondant', 'transfert_interne_o'], data = response.data;

        $.each(data, function(index, obj) {
            if (!weeks[obj['week']]) {
                weeks[obj['week']] = {};
            }
            $.each(sumCols, function (index, col) {
                if (!weeks[obj['week']][col]) {
                    weeks[obj['week']][col] = 0;
                }
                if (!columns[col]) {
                    columns[col] = 0;
                }
                var val = parseFloat(obj[col]);
                if (!isNaN(val)) {
                    weeks[obj['week']][col] += val;
                    columns[col] += val;
                }
            });
        });
    weeks = sortObject(weeks);
    return [weeks, columns];
}

function getsum2(response){
    var weeks = {},
        columns = {},
        sumCols = ['gueri', 'deces', 'abandon'], data = response.data;

        $.each(data, function(index, obj) {
            if (!weeks[obj['week']]) {
                weeks[obj['week']] = {};
            }
            $.each(sumCols, function (index, col) {
                if (!weeks[obj['week']][col]) {
                    weeks[obj['week']][col] = 0;
                }
                if (!columns[col]) {
                    columns[col] = 0;
                }
                var val = parseFloat(obj[col]);
                if (!isNaN(val)) {
                    weeks[obj['week']][col] += val;
                    columns[col] += val;
                }
            });
        });
    weeks = sortObject(weeks);
    return [weeks, columns];
}
// produce data for taux chart
function highchart_data_taux(sums) {
   var gueris = [], decess =[], abandons = [], weeks=[];
        $.each(sums, function (index, obj) {
          var somme_taux = obj.gueri + obj.deces + obj.abandon;
          var taux_guerison=(obj.gueri/somme_taux*100), taux_deces=(obj.deces/somme_taux*100), taux_abandon=(obj.abandon/somme_taux*100);
          gueris.push(Math.round(taux_guerison));
          decess.push(Math.round(taux_deces));
          abandons.push(Math.round(taux_abandon));
          weeks.push(index);
        });
        var donnees = [{data: gueris, name: "Taux de guerison"}, {data: decess,name: "Taux de deces"}, {data: abandons, name: "Taux d'abandons"}];
      return [donnees, weeks];
}

// produce data for tendances chart
function highchart_data_tendance(sums) {
   var admissions = [], sorties =[], fin_semaine = [], weeks=[];
        $.each(sums, function (index, obj) {
          var somme_admissions = obj.total_debut_semaine + obj.ptb + obj.oedemes + obj.rechute + obj.readmission + obj.transfert_interne_i
        ;
          var somme_sorties = obj.gueri + obj.deces + obj.abandon + obj.non_repondant + obj.transfert_interne_o;
          var somme_fin = somme_admissions - somme_sorties;
          admissions.push(Math.round(somme_admissions));
          sorties.push(Math.round(somme_sorties));
          fin_semaine.push(Math.round(somme_fin));
          weeks.push(index);
        });
        var donnees = [{data: admissions, name: "Admissions"}, {data: sorties,name: "Sorties"}, {data: fin_semaine, type: 'spline', name: "Total fin de semaine", marker: {lineWidth: 2, lineColor: Highcharts.getOptions().colors[3], fillColor: 'white'}}];
      return [donnees, weeks];
}

// Draw chart for taux
function draw_taux_chart(response, id, texte) {
  var sums = getsum2(response);
        var lesdonnees = highchart_data_taux(sums[0]);
        var sta_chart = Highcharts.chart(id, {
            chart: {
                type: 'spline'
            },
            credits: {
                text : "Unicef Burundi",
                href: "http://cmam.unicefburundi.org"
            },
            title: {
                text: texte
            },
            xAxis: {
                categories: lesdonnees[1]
            },
            plotOptions: {
                spline: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: false
                },
            },
            yAxis: {
                title: {
                    text: '%'
                }
            },
            series: lesdonnees[0]
        });
}

// Draw chart for taux
function draw_tendance_chart(response, id, texte) {
  var sums = getsum(response);
        var lesdonnees = highchart_data_tendance(sums[0]);
        var sta_chart = Highcharts.chart(id, {
            chart: {
                type: 'column'
            },
            credits: {
                text : "Unicef Burundi",
                href: "http://cmam.unicefburundi.org"
            },
            title: {
                text: texte
            },
            xAxis: {
                categories: lesdonnees[1],
                crosshair: true
            },
            plotOptions: {
                column: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: false
                },
            },
            yAxis: {
                title: {
                    text: 'Number of patients'
                }
            },
            series: lesdonnees[0]
        });
}

// Variables
 var  url_gen_taux_sta = "/cmam/outsum/?report__facility__facility_level__name=CDS",
        url_gen_taux_sst="/cmam/outsum/?report__facility__facility_level__name=Hospital",
        url_gen_tendance_sta = "/cmam/inoutreport/?facility__facility_level__name=CDS",
        url_gen_tendance_sst="/cmam/inoutreport/?facility__facility_level__name=Hospital",
        texte_taux_sta='Changing at rates STA',
        texte_taux_sst='Changing at rates SST',
        texte_tendance_sta='Trends in STA',
        texte_tendance_sst='Trends in SST',
        id_taux_sst='taux_sst',
        id_taux_sta='taux_sta',
        id_tendance_sta="tendance_sta",
        id_tendance_sst="tendance_sst";


var app = angular.module('myApp', []);

app.controller('myCtrl', ['$scope', '$http', function($scope, $http) {

        // province
        $http.get("/bdiadmin/province/")
          .then(function (response) {
            if (response.data.length > 0) {
                $scope.provinces = response.data;
              } else {
                $("#province-group").hide();
                $http.get("/bdiadmin/district/")
                .then(function (response) {
                    $scope.districts = response.data;
                });
              }
            });

        $scope.update_province = function () {
            var province = $scope.dashboard.province;
            var district = $scope.dashboard.district;
            $scope.cdss = '';
            if (province) {
              $http.get("/cmam/provinces/" + province.code + "/" )
                .then(function (response) {
                    $scope.districts = response.data.etablissements;
              });
              //  out reports CDS
              $http.get(url_gen_taux_sta + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate + "&search=" + province.code)
                .then(function (response) {
                  return draw_taux_chart(response, id_taux_sta, texte_taux_sta);
              });
              // Out reports Hospital
              $http.get(url_gen_taux_sst + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate + "&search=" + province.code)
                .then(function (response) {
                  return draw_taux_chart(response, id_taux_sst, texte_taux_sst);
                });
              //  tendance reports CDS
              $http.get(url_gen_tendance_sta + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate + "&search=" + province.code)
                .then(function (response) {
                  return draw_tendance_chart(response, id_tendance_sta, texte_tendance_sta);
              });
              // tendance reports Hospital
              $http.get(url_gen_tendance_sst + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate + "&search=" + province.code)
                .then(function (response) {
                  return draw_tendance_chart(response, id_tendance_sst, texte_tendance_sst);
                });
            } else {
              $scope.districts = '';
              $scope.cdss = '';
              //  out reports CDS
              $http.get(url_gen_taux_sta + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
              .then(function (response) {
                  return draw_taux_chart(response, id_taux_sta, texte_taux_sta);
              });
              //  tendance reports CDS
              $http.get(url_gen_tendance_sta + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
              .then(function (response) {
                  return draw_tendance_chart(response, id_tendance_sta, texte_tendance_sta);
              });
              // Out reports Hospital
              $http.get(url_gen_taux_sst + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
                .then(function (response) {
                  return draw_taux_chart(response, id_taux_sst, texte_taux_sst);
                });
              //  tendance reports Hospital
              $http.get(url_gen_tendance_sst  + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
              .then(function (response) {
                  return draw_tendance_chart(response, id_tendance_sst, texte_tendance_sst);
              });
            }
        };
          // district
        $scope.update_district = function () {
            var district = $scope.dashboard.district;
            $scope.cdss = '';
            if (district) {
              $http.get("/cmam/districts/" + district.code + "/" )
                .then(function (response) {
                  $scope.cdss = response.data.etablissements;
              });
              //  out reports CDS
              $http.get(url_gen_taux_sta + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate + "&search=" + district.code)
              .then(function (response) {
                  return draw_taux_chart(response, id_taux_sta, texte_taux_sta);
              });
              // Out reports Hospital
              $http.get(url_gen_taux_sst + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate + "&search=" + district.code)
                .then(function (response) {
                  return draw_taux_chart(response, id_taux_sst, texte_taux_sst);
                });
              //  tendance reports CDS
              $http.get(url_gen_tendance_sta + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate + "&search=" + district.code)
                .then(function (response) {
                  return draw_tendance_chart(response, id_tendance_sta, texte_tendance_sta);
              });
              // tendance reports Hospital
              $http.get(url_gen_tendance_sst + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate + "&search=" + district.code)
                .then(function (response) {
                  return draw_tendance_chart(response, id_tendance_sst, texte_tendance_sst);
                });
            } else {
              console.log($scope.dashboard.district);
            }
        };

        // cds
        $scope.update_cds = function () {
          console.log($scope)
            var cds = $scope.dashboard.cds;
            if (cds) {
              $http.get("/cmam/cdss/" + cds.code + "/" )
                .then(function (response) {
                  $scope.cds = response.data;
              });
              //  out reports CDS
              $http.get(url_gen_taux_sta + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate + "&search=" + cds.code)
              .then(function (response) {
                  return draw_taux_chart(response, id_taux_sta, texte_taux_sta);
              });
              // Out reports Hospital
              $http.get(url_gen_taux_sst + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate + "&search=" + cds.code)
                .then(function (response) {
                  return draw_taux_chart(response, id_taux_sst, texte_taux_sst);
                });
              //  tendance reports CDS
              $http.get(url_gen_tendance_sta + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate + "&search=" + cds.code)
                .then(function (response) {
                  return draw_tendance_chart(response, id_tendance_sta, texte_tendance_sta);
              });
              // tendance reports Hospital
              $http.get(url_gen_tendance_sst + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate + "&search=" + cds.code)
                .then(function (response) {
                  return draw_tendance_chart(response, id_tendance_sst, texte_tendance_sst);
                });
            } else {
              console.log($scope.dashboard.cds);
            }
        };

        $scope.get_by_date = function () {
          //  out reports CDS
          $http.get(url_gen_taux_sta + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
          .then(function (response) {
              return draw_taux_chart(response, id_taux_sta, texte_taux_sta);
          });
          //  tendance reports CDS
          $http.get(url_gen_tendance_sta  + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
          .then(function (response) {
              return draw_tendance_chart(response, id_tendance_sta, texte_tendance_sta);
          });
          // Out reports Hospital
          $http.get(url_gen_taux_sst + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
            .then(function (response) {
              return draw_taux_chart(response, id_taux_sst, texte_taux_sst);
            });
          //  tendance reports Hospital
          $http.get(url_gen_tendance_sst  + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
          .then(function (response) {
              return draw_tendance_chart(response, id_tendance_sst, texte_tendance_sst);
          });
        };
}]);




app.controller('DashCtrl', ['$scope', '$http', function($scope, $http) {
    //  out reports CDS
    $http.get(url_gen_taux_sta)
    .then(function (response) {
        return draw_taux_chart(response, id_taux_sta, texte_taux_sta);
    });
    //  tendance reports CDS
    $http.get(url_gen_tendance_sta )
    .then(function (response) {
        return draw_tendance_chart(response, id_tendance_sta, texte_tendance_sta);
    });
    // Out reports Hospital
    $http.get(url_gen_taux_sst)
      .then(function (response) {
        return draw_taux_chart(response, id_taux_sst, texte_taux_sst);
      });
    //  tendance reports Hospital
    $http.get(url_gen_tendance_sst )
    .then(function (response) {
        return draw_tendance_chart(response, id_tendance_sst, texte_tendance_sst);
    });
}]);

app.controller('ExportCtrl', ['$scope', '$http', 'DTOptionsBuilder', function($scope, $http, DTOptionsBuilder) {$scope.dtOptions = DTOptionsBuilder.newOptions().withPaginationType('full_numbers').withButtons([ 'copy', 'csv', 'excel', 'pdf', 'print']).withDOM("<'row'<'col-sm-3'l><'col-sm-4'i><'col-sm-5'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-4'B><'col-sm-8'p>>").withDisplayLength(50);
  }]);