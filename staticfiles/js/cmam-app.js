function sortObject(o) {
    return Object.keys(o).sort().reduce((r, k) => (r[k] = o[k], r), {});
}

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

var app = angular.module('myApp', []);

app.controller('myCtrl', ['$scope', '$http', function($scope, $http) {
        // years
        $http.get("/cmam/get_year/")
        .then(function (response) {
          $scope.years = response.data;
        });

        // province
        $http.get("/bdiadmin/province/")
          .then(function (response) {
              $scope.provinces = response.data;
          });

          $scope.update_province = function () {
            var province = $scope.dashboard.province;
            if (province) {
              $http.get("/cmam/provinces/" + province.code + "/" )
                .then(function (response) {
                    $scope.districts = response.data.districts;
              });
            }
        };
          // district
        $scope.update_district = function () {
            var district = $scope.dashboard.district;
            if (district) {
              $http.get("/cmam/districts/" + district.code + "/" )
                .then(function (response) {
                  $scope.cdss = response.data.cds;

              });
            }
        };

        // district
        $scope.update_district = function () {
            var district = $scope.dashboard.cds;
            if (district) {
              $http.get("/cmam/districts/" + district.code + "/" )
                .then(function (response) {
                  $scope.cdss = response.data.cds;
              });
            }
        };

        // weeks
        $http.get("/cmam/get_week/")
        .then(function (response) {
          $scope.weeks = response.data;
        });

        $scope.update_years = function () {
        };

        $scope.update_weeks = function () {
        };
}]);


app.controller('DashCtrl', ['$scope', '$http', function($scope, $http) {
    //  out reports CDS
    $http.get("/cmam/outsum/?report__facility__facility_level__name=CDS")
    .then(function (response) {
        var sums = getsum2(response);
        var gueris = [], decess =[], abandons = [], weeks=[];

        $.each(sums[0], function (index, obj) {
          // body...
          var somme_taux = obj.gueri + obj.deces + obj.abandon;
          var taux_guerison=(obj.gueri/somme_taux*100), taux_deces=(obj.deces/somme_taux*100), taux_abandon=(obj.abandon/somme_taux*100);
          gueris.push(Math.round(taux_guerison));
          decess.push(Math.round(taux_deces));
          abandons.push(Math.round(taux_abandon));
          weeks.push(index);
        });
        var donnees = [{data: gueris, name: "Taux de guerison"}, {data: decess,name: "Taux de deces"}, {data: abandons, name: "Taux d'abandons"}];

        var myChart = Highcharts.chart('container_sta', {
            chart: {
                type: 'spline'
            },
            title: {
                text: 'Evolution par semaine des taux au niveau STA'
            },
            xAxis: {
                categories: weeks
            },
            plotOptions: {
                spline: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                },
            },
            yAxis: {
                title: {
                    text: '%'
                }
            },
            series: donnees
        });
    });
    // Out reports Hospital
    $http.get("/cmam/outsum/?report__facility__facility_level__name=Hospital")
      .then(function (response) {
          var sums = getsum2(response);
          var gueris = [], decess =[], abandons = [], weeks=[];

          $.each(sums[0], function (index, obj) {
            // body...
            var somme_taux = obj.gueri + obj.deces + obj.abandon;
            var taux_guerison= ~~(obj.gueri/somme_taux*100), taux_deces= ~~(obj.deces/somme_taux*100), taux_abandon= ~~(obj.abandon/somme_taux*100);
            gueris.push(Math.round(taux_guerison));
            decess.push(Math.round(taux_deces));
            abandons.push(Math.round(taux_abandon));
            weeks.push(index);
          });
          var donnees = [{data: gueris, name: "Taus de guerison"}, {data: decess,name: "Taux de deces"}, {data: abandons,name: "Taux d'abandons"}];
          // console.log(donnees);

          var myChart = Highcharts.chart('container_sst', {
              chart: {
                  type: 'spline'
              },
              title: {
                  text: 'Evolution par semaine des taux au niveau SST'
              },
              xAxis: {
                  categories: weeks
              },
              plotOptions: {
                  spline: {
                      dataLabels: {
                          enabled: true
                      },
                      enableMouseTracking: true
                  }
              },
              yAxis: {
                  title: {
                      text: '%'
                  }
              },
              series: donnees
          });
      });
}]);